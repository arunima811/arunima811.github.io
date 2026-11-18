#!/usr/bin/env python3
"""Read-only GitHub Search/REST pull. Every call runs as: GH_TOKEN=<token> gh api -i <path>; set GH_TOKEN to use your own.

Subcommands: selftest | branchcheck | monthly base|branch [max_seconds] | samples | validate | summarize
"""
import calendar
import csv
import datetime as dt
import fcntl
import json
import math
import os
import statistics
import subprocess
import sys
import time
import urllib.parse
from collections import Counter

SCR = os.path.dirname(os.path.abspath(__file__))
API = os.path.join(os.path.dirname(SCR), 'data', 'api')
DATA = os.path.dirname(API)
LOG = os.path.join(API, 'queries.log')
LOCK = os.path.join(SCR, '.search_pace')
MPROG = os.path.join(SCR, 'monthly_progress.jsonl')
SPROG = os.path.join(SCR, 'samples_progress.jsonl')
SEARCH_GAP, CORE_GAP = float(os.environ.get('SEARCH_GAP', '2.3')), 0.8
LOG_HEADER = 'ts_utc\tkind\tpath_as_requested\tq_decoded\thttp_status\tresult\tattempt\tnote\n'
_state = {'tok': None, 'last_core': 0.0}

BASE = [
    ('merged_prs', 'search/issues', 'is:pr is:merged merged:{r}'),
    ('opened_prs', 'search/issues', 'is:pr created:{r}'),
    ('new_repos', 'search/repositories', 'created:{r}'),
    ('copilot_agent', 'search/issues', 'is:pr created:{r} author:app/copilot-swe-agent'),
    ('jules', 'search/issues', 'is:pr created:{r} author:app/google-labs-jules'),
    ('devin', 'search/issues', 'is:pr created:{r} author:app/devin-ai-integration'),
    ('codex', 'search/issues', 'is:pr created:{r} "chatgpt.com/codex" in:body'),
    ('claude_code', 'search/issues', 'is:pr created:{r} "Generated with Claude Code" in:body'),
    ('cursor_agents', 'search/issues', 'is:pr created:{r} "cursor.com/agents" in:body'),
    ('cursor_background_agent', 'search/issues', 'is:pr created:{r} "cursor.com/background-agent" in:body'),
]
PREFIXES = ('codex', 'copilot', 'claude', 'cursor', 'devin')
BRANCH = [(f'branch_{p}', 'search/issues', f'is:pr created:{{r}} head:{p}/') for p in PREFIXES]
AGENT_LOGINS = {'Copilot': 'copilot_agent', 'copilot-swe-agent[bot]': 'copilot_agent',
                'google-labs-jules[bot]': 'jules', 'devin-ai-integration[bot]': 'devin'}


def now():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def token():
    if _state['tok'] is None:
        _state['tok'] = os.environ.get('GH_TOKEN') or subprocess.run(
            ['gh', 'auth', 'token', '--hostname', 'github.com', '--user', 'arunima811'],
            capture_output=True, text=True, check=True).stdout.strip()
    return _state['tok']


def log(kind, path, q, status, result, attempt, note=''):
    try:
        fd = os.open(LOG, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        os.write(fd, LOG_HEADER.encode())
        os.close(fd)
    except FileExistsError:
        pass
    fields = [now(), kind, path, q, status, result, attempt, note]
    line = '\t'.join(str(f).replace('\t', ' ').replace('\n', ' ') for f in fields) + '\n'
    fd = os.open(LOG, os.O_WRONLY | os.O_APPEND)
    try:
        os.write(fd, line.encode())
    finally:
        os.close(fd)


def append_jsonl(path, obj):
    with open(path, 'a') as f:
        f.write(json.dumps(obj) + '\n')


def load_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        out = []
        for line in f:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        return out


def pace(kind):
    if kind == 'core':
        wait = _state['last_core'] + CORE_GAP - time.time()
        if wait > 0:
            time.sleep(wait)
        _state['last_core'] = time.time()
        return
    with open(LOCK, 'a+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        s = f.read().strip()
        wait = (float(s) if s else 0.0) + SEARCH_GAP - time.time()
        if wait > 0:
            time.sleep(wait)
        f.seek(0)
        f.truncate()
        f.write(repr(time.time()))
        f.flush()
        fcntl.flock(f, fcntl.LOCK_UN)


def gh_get(path):
    env = dict(os.environ, GH_TOKEN=token())
    p = subprocess.run(['gh', 'api', '-i', path], capture_output=True, text=True, env=env, timeout=120)
    out = p.stdout.replace('\r\n', '\n')
    head, _, body = out.partition('\n\n')
    lines = head.split('\n')
    status = None
    if lines and lines[0].startswith('HTTP'):
        try:
            status = int(lines[0].split()[1])
        except (IndexError, ValueError):
            status = None
    headers = {}
    for line in lines[1:]:
        k, sep, v = line.partition(':')
        if sep:
            headers[k.strip().lower()] = v.strip()
    try:
        data = json.loads(body) if body.strip() else None
    except json.JSONDecodeError:
        data = None
    return status, headers, data, p.stderr.strip()


def backoff(status, headers, attempt):
    if 'retry-after' in headers:
        return float(headers['retry-after']) + 1
    if headers.get('x-ratelimit-remaining') == '0' and 'x-ratelimit-reset' in headers:
        return max(1.0, int(headers['x-ratelimit-reset']) - time.time() + 2)
    if status in (403, 429):
        return min(60 * 2 ** (attempt - 1), 600)
    return min(10 * 2 ** (attempt - 1), 300)


def request(kind, path, q=''):
    for attempt in range(1, 9):
        pace(kind)
        try:
            status, headers, data, err = gh_get(path)
        except subprocess.TimeoutExpired:
            status, headers, data, err = None, {}, None, 'timeout'
        if status == 200 and data is not None:
            low = 0 if kind == 'search' else 50
            if int(headers.get('x-ratelimit-remaining', '999')) <= low and 'x-ratelimit-reset' in headers:
                time.sleep(max(0.0, int(headers['x-ratelimit-reset']) - time.time()) + 1)
            return status, headers, data, attempt
        msg = (data.get('message', '') if isinstance(data, dict) else '') or err[:200]
        retryable = status is None or status >= 500 or status == 429 or (
            status == 403 and any(w in msg.lower() for w in ('rate limit', 'abuse', 'secondary')))
        if not retryable or attempt == 8:
            log(kind, path, q, status, 'ERROR', attempt, msg[:200])
            return status, headers, data, attempt
        wait = backoff(status, headers, attempt)
        log(kind, path, q, status, 'RETRY', attempt, f'{msg[:150]}; backoff {wait:.0f}s')
        time.sleep(wait)
    return None, {}, None, 8


def search(endpoint, q, per_page=1, page=None):
    path = f'{endpoint}?q={urllib.parse.quote(q, safe="")}&per_page={per_page}' + (f'&page={page}' if page else '')
    status, _, data, attempt = request('search', path, q)
    if status == 200:
        log('search', path, q, status,
            f'total_count={data["total_count"]};incomplete_results={data["incomplete_results"]}', attempt)
        return data
    return None


def get_pr(repo, num):
    path = f'repos/{repo}/pulls/{num}'
    status, _, data, attempt = request('core', path)
    if status == 200:
        u = data.get('user') or {}
        log('core', path, '', status,
            f'additions={data["additions"]};deletions={data["deletions"]};changed_files={data["changed_files"]};'
            f'user_type={u.get("type", "")};head_ref={data["head"]["ref"]}', attempt)
        return status, data
    return status, None


def items_of(d):
    return [(it['repository_url'].split('/repos/', 1)[1], it['number'], it['created_at'][:10])
            for it in (d or {}).get('items', [])]


def months(a='2022-01', b='2026-10'):
    y, m = map(int, a.split('-'))
    yb, mb = map(int, b.split('-'))
    while (y, m) <= (yb, mb):
        yield f'{y:04d}-{m:02d}'
        m += 1
        if m == 13:
            y, m = y + 1, 1


def month_bounds(mo):
    y, m = map(int, mo.split('-'))
    return f'{mo}-01', f'{mo}-15', f'{mo}-16', f'{mo}-{calendar.monthrange(y, m)[1]:02d}'


def count_metric(endpoint, tmpl, mo):
    a, h1, h2, z = month_bounds(mo)
    q = tmpl.format(r=f'{a}..{z}')
    d = search(endpoint, q)
    if d is None:
        return None, 'error'
    if not d['incomplete_results']:
        return d['total_count'], 'ok'
    d = search(endpoint, q)
    if d is not None and not d['incomplete_results']:
        return d['total_count'], 'retry_ok'
    total, inc = 0, False
    for rng in (f'{a}..{h1}', f'{h2}..{z}'):
        hq = tmpl.format(r=rng)
        hd = search(endpoint, hq)
        if hd is not None and hd['incomplete_results']:
            hd = search(endpoint, hq)
        if hd is None:
            return None, 'error'
        total += hd['total_count']
        inc = inc or hd['incomplete_results']
    return total, 'split_incomplete' if inc else 'split'


def write_monthly():
    rec = {(r['month'], r['metric']): r for r in load_jsonl(MPROG)}
    metrics = [m for m, _, _ in BASE + BRANCH if any(k[1] == m for k in rec)]
    with open(os.path.join(API, 'monthly.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['month'] + metrics + [f'{m}_flag' for m in metrics])
        for mo in months():
            vals = [rec.get((mo, m), {}).get('count', '') for m in metrics]
            vals = ['' if v is None else v for v in vals]
            flags = [rec.get((mo, m), {}).get('flag', 'missing') for m in metrics]
            w.writerow([mo] + vals + flags)


def monthly(which, max_seconds, start='2022-01'):
    t0 = time.time()
    specs = BASE if which == 'base' else BRANCH
    done = {(r['month'], r['metric']) for r in load_jsonl(MPROG) if r['flag'] != 'error'}
    todo = [(mo, s) for mo in months(start) for s in specs if (mo, s[0]) not in done]
    ran = 0
    for mo, (metric, ep, tmpl) in todo:
        if time.time() - t0 > max_seconds:
            break
        count, flag = count_metric(ep, tmpl, mo)
        append_jsonl(MPROG, {'month': mo, 'metric': metric, 'endpoint': ep, 'template': tmpl,
                             'count': count, 'flag': flag})
        ran += 1
    write_monthly()
    flags = Counter(r['flag'] for r in load_jsonl(MPROG) if r['metric'] in {s[0] for s in specs})
    print(f'monthly {which}: ran {ran}, remaining {len(todo) - ran}; flags {dict(flags)}')


def branchcheck():
    tools = [('codex', '"chatgpt.com/codex" in:body'), ('copilot', 'author:app/copilot-swe-agent'),
             ('claude', '"Generated with Claude Code" in:body'), ('cursor', '"cursor.com/agents" in:body'),
             ('devin', 'author:app/devin-ai-integration')]
    rng = 'created:2025-10-01..2025-10-31'
    out = []
    for p, tq in tools:
        known, nref = [], 0
        for repo, num, cdate in items_of(search('search/issues', f'is:pr {rng} {tq}', per_page=8)):
            _, pr = get_pr(repo, num)
            if pr is None:
                continue
            nref += 1
            if pr['head']['ref'].lower().startswith(p + '/'):
                known.append((repo, num, cdate, pr['head']['ref']))
        rec = {'slash': 0, 'noslash': 0, 'exact': 0}
        tested = known[:3]
        for repo, num, cdate, ref in tested:
            for k, h in (('slash', f'{p}/'), ('noslash', p), ('exact', ref)):
                dd = search('search/issues', f'is:pr repo:{repo} created:{cdate} head:{h}', per_page=100)
                if dd and any(it['number'] == num for it in dd['items']):
                    rec[k] += 1
        dg = search('search/issues', f'is:pr {rng} head:{p}/', per_page=20)
        dn = search('search/issues', f'is:pr {rng} head:{p}', per_page=1)
        match, n, odd = 0, 0, []
        for repo, num, _ in items_of(dg):
            _, pr = get_pr(repo, num)
            if pr is None:
                continue
            n += 1
            if pr['head']['ref'].lower().startswith(p + '/'):
                match += 1
            else:
                odd.append(pr['head']['ref'])
        out.append({'prefix': p, 'tool_query': tq, 'tool_prs_using_prefix': f'{len(known)}/{nref}',
                    'recall_tested': len(tested), 'recall_head_prefix_slash': rec['slash'],
                    'recall_head_prefix_noslash': rec['noslash'], 'recall_head_exact_ref': rec['exact'],
                    'oct2025_count_head_slash': dg and dg['total_count'],
                    'oct2025_count_head_noslash': dn and dn['total_count'],
                    'precision_sample_n': n, 'precision_ref_starts_with_prefix': match,
                    'example_known_ref': tested[0][3] if tested else '', 'nonmatching_refs': '|'.join(odd[:5])})
    q0 = 'is:pr is:merged merged:2025-09-01..2025-09-30'
    a, b = search('search/issues', q0), search('search/issues', q0 + ' is:public')
    out.append({'prefix': 'is_public_check', 'tool_query': q0,
                'oct2025_count_head_slash': a and a['total_count'],
                'oct2025_count_head_noslash': b and b['total_count']})
    with open(os.path.join(API, 'branch_prefix_check.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    for r in out:
        print({k: v for k, v in r.items() if k != 'tool_query'})


def agent_marker(login, body, ref):
    if login in AGENT_LOGINS:
        return AGENT_LOGINS[login]
    b = body or ''
    if 'chatgpt.com/codex' in b:
        return 'codex'
    if 'Generated with [Claude Code]' in b or 'Generated with Claude Code' in b:
        return 'claude_code'
    if 'cursor.com/agents' in b or 'cursor.com/background-agent' in b:
        return 'cursor'
    for p in PREFIXES:
        if (ref or '').lower().startswith(p + '/'):
            return 'branch_' + p
    return ''


SAMPLE_MONTHS = ['2023-03', '2024-03', '2025-03'] + list(months('2025-10', '2026-10'))


def samples():
    recs = load_jsonl(SPROG)
    windows = {r['wid']: r for r in recs if r['type'] == 'window' and r.get('total_count') is not None}
    done = {(r['wid'], r['repo'], r['number']) for r in recs
            if r['type'] == 'pr' and r['http_status'] in (200, 403, 404, 410, 451)}
    for mo in SAMPLE_MONTHS:
        for day in (10, 20):
            wid = f'{mo}-{day:02d}'
            if wid not in windows:
                q = f'is:pr is:merged merged:{wid}T15:00:00Z..{wid}T16:00:00Z'
                d = search('search/issues', q, per_page=50, page=1)
                rec = {'type': 'window', 'wid': wid, 'month': mo, 'q': q,
                       'total_count': d['total_count'] if d else None,
                       'incomplete': d['incomplete_results'] if d else None,
                       'items': [[r, n] for r, n, _ in items_of(d)]}
                append_jsonl(SPROG, rec)
                if d is None:
                    continue
                windows[wid] = rec
            for rank, (repo, num) in enumerate(windows[wid]['items'], 1):
                if (wid, repo, num) in done:
                    continue
                status, pr = get_pr(repo, num)
                row = {'type': 'pr', 'month': mo, 'wid': wid, 'rank': rank, 'repo': repo, 'number': num,
                       'http_status': status}
                if pr is not None:
                    u = pr.get('user') or {}
                    row.update(created_at=pr['created_at'], merged_at=pr['merged_at'],
                               additions=pr['additions'], deletions=pr['deletions'],
                               changed_files=pr['changed_files'], commits=pr['commits'],
                               user_login=u.get('login', ''), user_type=u.get('type', ''),
                               head_ref=pr['head']['ref'],
                               agent_marker=agent_marker(u.get('login', ''), pr.get('body'), pr['head']['ref']))
                append_jsonl(SPROG, row)
                done.add((wid, repo, num))
    write_samples()


def med(xs):
    return statistics.median(xs) if xs else ''


def med_ci(xs):
    xs = sorted(xs)
    n = len(xs)
    if n < 6:
        return '', ''
    j = max(1, round(n / 2 - 0.98 * math.sqrt(n)))
    k = min(n, round(n / 2 + 0.98 * math.sqrt(n)) + 1)
    return xs[j - 1], xs[k - 1]


def pct(a, b):
    return round(100 * a / b, 1) if b else ''


def write_samples():
    recs = load_jsonl(SPROG)
    wins = {r['wid']: r for r in recs if r['type'] == 'window' and r.get('total_count') is not None}
    prs = {(r['wid'], r['repo'], r['number']): r for r in recs if r['type'] == 'pr'}
    rows = sorted(prs.values(), key=lambda r: (r['wid'], r['rank']))
    cols = ['month', 'wid', 'rank', 'repo', 'number', 'http_status', 'created_at', 'merged_at', 'additions',
            'deletions', 'changed_files', 'commits', 'user_login', 'user_type', 'head_ref', 'agent_marker']
    with open(os.path.join(API, 'pr_samples.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    out = []
    for mo in SAMPLE_MONTHS:
        ok = [r for r in rows if r['month'] == mo and r['http_status'] == 200]
        nb = [r for r in ok if r['user_type'] != 'Bot']
        add, addnb = [r['additions'] for r in ok], [r['additions'] for r in nb]
        lo, hi = med_ci(add)
        lo2, hi2 = med_ci(addnb)
        inwin = sum(1 for r in ok if f"{r['wid']}T15:00:00Z" <= r['merged_at'] <= f"{r['wid']}T16:00:00Z")
        out.append({'month': mo,
                    'window_total_counts': '|'.join(str(wins.get(f'{mo}-{d}', {}).get('total_count', ''))
                                                    for d in ('10', '20')),
                    'n': len(ok), 'median_additions': med(add), 'add_ci95_lo': lo, 'add_ci95_hi': hi,
                    'median_deletions': med([r['deletions'] for r in ok]),
                    'median_changed_files': med([r['changed_files'] for r in ok]),
                    'median_add_plus_del': med([r['additions'] + r['deletions'] for r in ok]),
                    'n_nonbot': len(nb), 'median_additions_nonbot': med(addnb),
                    'nonbot_ci95_lo': lo2, 'nonbot_ci95_hi': hi2,
                    'bot_share_pct': pct(len(ok) - len(nb), len(ok)),
                    'agent_marker_share_pct': pct(sum(1 for r in ok if r.get('agent_marker')), len(ok)),
                    'merged_in_window_pct': pct(inwin, len(ok))})
    with open(os.path.join(API, 'pr_sizes.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    for r in out:
        print(','.join(str(r[k]) for k in ('month', 'window_total_counts', 'n', 'median_additions', 'add_ci95_lo',
                                            'add_ci95_hi', 'n_nonbot', 'median_additions_nonbot',
                                            'bot_share_pct', 'agent_marker_share_pct', 'merged_in_window_pct')))


def read_csv(p):
    with open(p, newline='') as f:
        return list(csv.DictReader(f))


def ratio(a, b):
    return round(float(a) / float(b), 4) if a not in ('', None) and b not in ('', None) and float(b) else ''


def validate():
    api = {r['month']: r for r in read_csv(os.path.join(API, 'monthly.csv'))}
    gha = {r['month']: r for r in read_csv(os.path.join(DATA, 'monthly.csv'))}
    rows = []
    for mo in list(months('2023-02', '2024-05')) + list(months('2025-11', '2026-02')):
        g, a = gha.get(mo, {}), api.get(mo, {})
        rows.append({'month': mo, 'gha_coverage_status': g.get('coverage_status', ''),
                     'gha_prs_merged_fixed': g.get('prs_merged_fixed', ''), 'search_merged_prs': a.get('merged_prs', ''),
                     'ratio_merged_gha_over_search': ratio(g.get('prs_merged_fixed'), a.get('merged_prs')),
                     'gha_prs_merged_action': g.get('prs_merged_action', ''),
                     'ratio_merged_action_gha_over_search': ratio(g.get('prs_merged_action'), a.get('merged_prs')),
                     'gha_prs_opened': g.get('prs_opened', ''), 'search_opened_prs': a.get('opened_prs', ''),
                     'ratio_opened_gha_over_search': ratio(g.get('prs_opened'), a.get('opened_prs')),
                     'gha_new_repos': g.get('new_repos', ''), 'search_new_repos': a.get('new_repos', ''),
                     'ratio_repos_gha_over_search': ratio(g.get('new_repos'), a.get('new_repos'))})
    ag = {r['month']: r for r in read_csv(os.path.join(DATA, 'agent_prs_monthly.csv'))}
    mo = '2026-01'
    for gcol, scol in (('copilot_coding_agent', 'copilot_agent'), ('google_jules', 'jules'), ('devin', 'devin')):
        gv, sv = ag.get(mo, {}).get(gcol, ''), api.get(mo, {}).get(scol, '')
        rows.append({'month': f'{mo} agent:{scol}', 'gha_coverage_status': ag.get(mo, {}).get('coverage_status', ''),
                     'gha_prs_opened': gv, 'search_opened_prs': sv, 'ratio_opened_gha_over_search': ratio(gv, sv)})
    with open(os.path.join(API, 'validation_vs_gharchive.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r['month'], r['gha_coverage_status'], r.get('ratio_merged_gha_over_search', ''),
              r.get('ratio_opened_gha_over_search', ''), r.get('ratio_repos_gha_over_search', ''),
              r.get('gha_prs_opened', ''), r.get('search_opened_prs', ''))


def summarize():
    by = {r['month']: r for r in read_csv(os.path.join(API, 'monthly.csv'))}

    def num(mo, m):
        v = by.get(mo, {}).get(m, '')
        return int(v) if v not in ('', None) else 0

    for m in ('merged_prs', 'opened_prs', 'new_repos'):
        prev = prev_jo = None
        for y in range(2022, 2027):
            last = 12 if y < 2026 else 10
            tot = sum(num(f'{y}-{i:02d}', m) for i in range(1, last + 1))
            jo = sum(num(f'{y}-{i:02d}', m) for i in range(1, 11))
            yoy = f'{100 * (tot / prev - 1):.1f}%' if prev and y < 2026 else ''
            yoy_jo = f'{100 * (jo / prev_jo - 1):.1f}%' if prev_jo else ''
            print(f'{m} {y}: total {tot:,} avg/mo {tot // last:,} janoct {jo:,} yoy_full {yoy} yoy_janoct {yoy_jo}')
            prev, prev_jo = tot, jo
    agents = [s[0] for s in BASE[3:]] + [s[0] for s in BRANCH if s[0] in by.get('2026-10', {})]
    for a in agents:
        series = [(mo, num(mo, a)) for mo in months('2024-01', '2026-10')]
        peak = max(series, key=lambda t: t[1])
        jo26 = sum(num(f'2026-{i:02d}', a) for i in range(1, 11))
        op26 = sum(num(f'2026-{i:02d}', 'opened_prs') for i in range(1, 11))
        first = next((mo for mo, v in series if v >= 100), '')
        print(f'{a}: first>=100 {first}; 2025-10 {num("2025-10", a):,}; 2026-10 {num("2026-10", a):,} '
              f'({100 * num("2026-10", a) / max(1, num("2026-10", "opened_prs")):.2f}% of opened); '
              f'janoct26 {jo26:,} ({100 * jo26 / max(1, op26):.2f}%); peak {peak[0]} {peak[1]:,}')
    for mo in ('2024-10', '2025-04', '2025-07', '2025-10', '2026-01', '2026-04', '2026-07', '2026-10'):
        tot = sum(num(mo, s[0]) for s in BASE[3:])
        print(f'{mo}: opened {num(mo, "opened_prs"):,} merged {num(mo, "merged_prs"):,} '
              f'repos {num(mo, "new_repos"):,} agent_sum {tot:,} ({100 * tot / max(1, num(mo, "opened_prs")):.2f}%)')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'selftest':
        st, hd, dat, att = request('core', 'rate_limit')
        log('core', 'rate_limit', '', st, f'search_remaining={dat["resources"]["search"]["remaining"]}', att)
        print(st, hd.get('x-ratelimit-resource'), dat['resources']['search'], dat['resources']['core']['remaining'])
    elif cmd == 'branchcheck':
        branchcheck()
    elif cmd == 'monthly':
        monthly(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1e9,
                sys.argv[4] if len(sys.argv) > 4 else '2022-01')
    elif cmd == 'samples':
        samples()
    elif cmd == 'validate':
        validate()
    elif cmd == 'summarize':
        summarize()
