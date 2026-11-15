#!/usr/bin/env python3
"""Fill the playground gap (2024-06-05 .. 2025-09-25) for A3 with raw GH Archive samples.

Samples the 15th of each month at 03:00 and 15:00 UTC, one file at a time (download to
data/_tmp, process, delete). Per hour it counts opened PRs, merged PRs, AI-tool body
signatures (same case-insensitive substrings as the playground query), AI-agent logins
(same product mapping as q_a3_agent_prs_monthly.sql) and agent branch prefixes.
Appends one JSON record per hour to data/work/signature_sample_hours.jsonl (resumable).
"""
import collections
import datetime
import gzip
import json
import os
import subprocess
import sys
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
TMP_DIR = os.path.join(DATA_DIR, "_tmp")
OUT_PATH = os.path.join(DATA_DIR, "work", "signature_sample_hours.jsonl")
BASE_URL = "https://data.gharchive.org"
HOURS = (3, 15)

SIGNATURES = {
    "sig_generated_with_claude_code": ["generated with [claude code]"],
    "sig_claude_ai_code_link": ["claude.ai/code"],
    "sig_claude_code_mention": ["claude code"],
    "sig_coauthored_by_claude": ["co-authored-by: claude"],
    "sig_codex_link": ["chatgpt.com/codex"],
    "sig_cursor_agent_link": ["cursor.com/background-agent", "cursor.com/agents"],
    "sig_devin_session_link": ["devin.ai/sessions"],
    "sig_jules_link": ["jules.google"],
    "sig_copilot_mention": ["copilot"],
}
SPECIFIC = ["claude code", "claude.ai/code", "co-authored-by: claude", "chatgpt.com/codex",
            "cursor.com/background-agent", "cursor.com/agents", "devin.ai/sessions", "jules.google"]

AGENTS = {
    "Copilot": "copilot_coding_agent",
    "google-labs-jules[bot]": "google_jules",
    "devin-ai-integration[bot]": "devin", "staging-devin-ai-integration[bot]": "devin",
    "cto-new[bot]": "cto_new",
    "sweep-ai[bot]": "sweep", "sweep-nightly[bot]": "sweep", "sweep-canary[bot]": "sweep",
    "claude[bot]": "claude_code_github_app",
    "Claude": "claude_agent_hq",
    "Codex": "codex_agent_hq",
    "cursor[bot]": "cursor_agent",
    "netlify-coding[bot]": "netlify_agent_runners",
    "codeflash-ai[bot]": "codeflash",
    "coderabbitai[bot]": "coderabbit",
    "e2b-for-github[bot]": "e2b",
    "snorkell-ai[bot]": "snorkell",
    "genspark-ai-developer[bot]": "genspark",
    "blitzy[bot]": "blitzy", "blitzy-qa[bot]": "blitzy",
    "jetbrains-junie[bot]": "jetbrains_junie",
    "opencode-agent[bot]": "opencode",
    "codegen-sh[bot]": "codegen",
    "kiro-agent[bot]": "kiro",
    "roomote[bot]": "roo_code_roomote", "roomote-v0[bot]": "roo_code_roomote",
    "tembo[bot]": "tembo",
    "kilo-code-bot[bot]": "kilo_code", "kiloconnect[bot]": "kilo_code",
    "amazon-q-developer[bot]": "amazon_q_developer",
    "factory-droid[bot]": "factory_droid",
    "capy-ai[bot]": "capy",
    "gitauto-ai[bot]": "gitauto",
    "ellipsis-dev[bot]": "ellipsis",
    "cubic-dev-ai[bot]": "cubic",
    "seer-by-sentry[bot]": "sentry_seer", "sentry-ai-autofix-experimental[bot]": "sentry_seer",
    "komment-ai[bot]": "komment", "komment-ai-dev[bot]": "komment", "komment-ai-beta[bot]": "komment",
    "codeant-ai[bot]": "codeant",
}
BRANCH_PREFIXES = ("claude/", "codex/", "copilot/", "cursor/", "devin/")


def planned_hours():
    hours = []
    month = datetime.date(2024, 6, 1)
    while month <= datetime.date(2025, 9, 1):
        for hour in HOURS:
            hours.append(datetime.datetime(month.year, month.month, 15, hour))
        month = (month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    return hours


def signature_hits(body_lower: str) -> dict:
    hits = {name: any(p in body_lower for p in pats) for name, pats in SIGNATURES.items()}
    hits["sig_any_specific"] = any(p in body_lower for p in SPECIFIC)
    hits["sig_any_incl_copilot"] = hits["sig_any_specific"] or hits["sig_copilot_mention"]
    return hits


def process_file(path: str) -> dict:
    opened = collections.Counter()
    merged = collections.Counter()
    agents = collections.Counter()
    branches = collections.Counter()
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if '"PullRequestEvent"' not in line:
                continue
            ev = json.loads(line)
            if ev.get("type") != "PullRequestEvent":
                continue
            payload = ev.get("payload") or {}
            action = payload.get("action")
            pr = payload.get("pull_request") or {}
            is_opened = action == "opened"
            is_merged = action == "closed" and pr.get("merged") is True
            if not (is_opened or is_merged):
                continue
            body = (pr.get("body") or "").lower()
            bucket = opened if is_opened else merged
            bucket["prs"] += 1
            if body:
                bucket["prs_with_body"] += 1
            for name, hit in signature_hits(body).items():
                if hit:
                    bucket[name] += 1
            if is_opened:
                login = (ev.get("actor") or {}).get("login") or ""
                product = AGENTS.get(login)
                if product:
                    agents[product] += 1
                head_ref = ((pr.get("head") or {}).get("ref") or "").lower()
                for prefix in BRANCH_PREFIXES:
                    if head_ref.startswith(prefix):
                        branches["branch_" + prefix.rstrip("/")] += 1
    return {"opened": dict(opened), "merged": dict(merged), "agents": dict(agents),
            "branches": dict(branches)}


def already_done():
    if not os.path.exists(OUT_PATH):
        return set()
    with open(OUT_PATH, encoding="utf-8") as fh:
        return {json.loads(line)["hour_utc"] for line in fh if line.strip()}


def main():
    os.makedirs(TMP_DIR, exist_ok=True)
    done = already_done()
    for ts in planned_hours():
        key = ts.strftime("%Y-%m-%d %H:00")
        if key in done:
            continue
        name = f"{ts:%Y-%m-%d}-{ts.hour}.json.gz"
        path = os.path.join(TMP_DIR, name)
        started = time.time()
        try:
            subprocess.run(["curl", "-sS", "--fail", "--retry", "5", "--retry-delay", "10",
                            "--max-time", "1200", "-o", path, f"{BASE_URL}/{name}"], check=True)
            record = process_file(path)
        except (subprocess.CalledProcessError, OSError, EOFError, gzip.BadGzipFile) as exc:
            print(f"FAILED {name}: {exc}", flush=True)
            continue
        finally:
            if os.path.exists(path):
                os.remove(path)
        record.update({"hour_utc": key, "weekday": ts.strftime("%a"), "is_weekend": ts.weekday() >= 5})
        with open(OUT_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
        print(f"done {name} opened={record['opened'].get('prs', 0)} "
              f"any_specific={record['opened'].get('sig_any_specific', 0)} ({time.time() - started:.0f}s)",
              flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    sys.exit(main())
