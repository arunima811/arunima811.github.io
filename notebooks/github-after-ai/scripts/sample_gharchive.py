#!/usr/bin/env python3
"""Source B: stream-process sampled GH Archive hours, one file at a time.

For each hour: download to data/_tmp, parse gzip JSON lines, compute metrics,
append one JSON record to data/work/sampled_hours.jsonl, delete the file.
Resumable: hours already present in the jsonl are skipped.
"""
import collections
import datetime
import gzip
import json
import os
import statistics
import subprocess
import sys
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
TMP_DIR = os.path.join(DATA_DIR, "_tmp")
OUT_PATH = os.path.join(DATA_DIR, "work", "sampled_hours.jsonl")
BASE_URL = "https://data.gharchive.org"
SAMPLE_MONTHS = (2, 5, 8, 11)
SAMPLE_DAY = 15
SAMPLE_HOUR = 15
MASS_PUSH_THRESHOLD = 1000


def planned_hours():
    hours = []
    for year in range(2015, 2026):
        role = "baseline" if year <= 2022 else "extension"
        for month in SAMPLE_MONTHS:
            hours.append((datetime.datetime(year, month, SAMPLE_DAY, SAMPLE_HOUR), role))
    for month in (2, 5):
        hours.append((datetime.datetime(2026, month, SAMPLE_DAY, SAMPLE_HOUR), "diagnostic"))
    return hours


def file_name(ts: datetime.datetime) -> str:
    return f"{ts:%Y-%m-%d}-{ts.hour}.json.gz"


def summarize(values):
    if not values:
        return None, None
    return round(statistics.fmean(values), 3), statistics.median(values)


def process_file(path: str, ts: datetime.datetime) -> dict:
    counts = collections.Counter()
    pushers = set()
    create_ref_types = collections.Counter()
    pr_actions = collections.Counter()
    merged_add, merged_del, merged_files = [], [], []
    push_sizes_sum = distinct_sum = capped_sum = 0
    max_push_size = 0
    min_created, max_created = None, None
    file_hour_prefix = ts.strftime("%Y-%m-%dT%H")

    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                counts["malformed_lines"] += 1
                continue
            counts["events_total"] += 1
            created = ev.get("created_at") or ""
            if not created.startswith(file_hour_prefix):
                counts["events_outside_file_hour"] += 1
            if created:
                min_created = created if min_created is None or created < min_created else min_created
                max_created = created if max_created is None or created > max_created else max_created
            etype = ev.get("type")
            payload = ev.get("payload") or {}
            actor = (ev.get("actor") or {}).get("login")

            if etype == "PushEvent":
                counts["push_events"] += 1
                pushers.add(actor)
                size = payload.get("size")
                if size is None:
                    counts["push_size_missing"] += 1
                    continue
                distinct = payload.get("distinct_size") or 0
                push_sizes_sum += size
                distinct_sum += distinct
                capped_sum += min(size, MASS_PUSH_THRESHOLD)
                max_push_size = max(max_push_size, size)
                if size >= MASS_PUSH_THRESHOLD:
                    counts["pushes_size_ge_1000"] += 1
                if size == 0:
                    counts["push_size_zero"] += 1
            elif etype == "CreateEvent":
                counts["create_events"] += 1
                ref_type = payload.get("ref_type")
                create_ref_types[str(ref_type)] += 1
            elif etype == "PullRequestEvent":
                counts["pr_events"] += 1
                action = payload.get("action")
                pr_actions[str(action)] += 1
                pr = payload.get("pull_request") or {}
                if action == "opened":
                    counts["prs_opened"] += 1
                    if "title" not in pr:
                        counts["prs_opened_without_title_field"] += 1
                elif action == "closed" and pr.get("merged") is True:
                    counts["prs_merged_closed_flag"] += 1
                    adds, dels = pr.get("additions"), pr.get("deletions")
                    if adds is None or dels is None:
                        counts["merged_size_missing"] += 1
                    else:
                        merged_add.append(adds)
                        merged_del.append(dels)
                        merged_files.append(pr.get("changed_files") or 0)
                elif action == "merged":
                    counts["prs_merged_action"] += 1

    avg_add, med_add = summarize(merged_add)
    avg_del, med_del = summarize(merged_del)
    avg_files, _ = summarize(merged_files)
    size_present = counts["push_events"] - counts["push_size_missing"]
    return {
        "hour_utc": ts.strftime("%Y-%m-%d %H:00"),
        "file": file_name(ts),
        "weekday": ts.strftime("%a"),
        "is_weekend": ts.weekday() >= 5,
        "events_total": counts["events_total"],
        "malformed_lines": counts["malformed_lines"],
        "events_outside_file_hour": counts["events_outside_file_hour"],
        "min_created_at": min_created,
        "max_created_at": max_created,
        "push_events": counts["push_events"],
        "push_size_missing": counts["push_size_missing"],
        "commits": push_sizes_sum if size_present else None,
        "distinct_commits": distinct_sum if size_present else None,
        "commits_cap1000": capped_sum if size_present else None,
        "pushes_size_ge_1000": counts["pushes_size_ge_1000"] if size_present else None,
        "push_size_zero": counts["push_size_zero"] if size_present else None,
        "max_push_size": max_push_size if size_present else None,
        "pushers": len(pushers),
        "create_events": counts["create_events"],
        "new_repos": create_ref_types.get("repository", 0),
        "create_ref_types": dict(create_ref_types),
        "pr_events": counts["pr_events"],
        "pr_actions": dict(pr_actions),
        "prs_opened": counts["prs_opened"],
        "prs_opened_without_title_field": counts["prs_opened_without_title_field"],
        "prs_merged_closed_flag": counts["prs_merged_closed_flag"],
        "prs_merged_action": counts["prs_merged_action"],
        "merged_size_missing": counts["merged_size_missing"],
        "merged_with_size": len(merged_add),
        "avg_additions": avg_add,
        "median_additions": med_add,
        "avg_deletions": avg_del,
        "median_deletions": med_del,
        "avg_changed_files": avg_files,
        "merged_additions": merged_add,
        "merged_deletions": merged_del,
    }


def already_done():
    if not os.path.exists(OUT_PATH):
        return set()
    with open(OUT_PATH, encoding="utf-8") as fh:
        return {json.loads(line)["hour_utc"] for line in fh if line.strip()}


def main():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    done = already_done()
    for ts, role in planned_hours():
        key = ts.strftime("%Y-%m-%d %H:00")
        if key in done:
            continue
        name = file_name(ts)
        path = os.path.join(TMP_DIR, name)
        started = time.time()
        try:
            subprocess.run(["curl", "-sS", "--fail", "--retry", "5", "--retry-delay", "10",
                            "--max-time", "1200", "-o", path, f"{BASE_URL}/{name}"], check=True)
            size_mb = os.path.getsize(path) / 1e6
            record = process_file(path, ts)
            record["role"] = role
            record["gz_mb"] = round(size_mb, 1)
        except (subprocess.CalledProcessError, OSError, EOFError, gzip.BadGzipFile) as exc:
            print(f"FAILED {name}: {exc}", flush=True)
            continue
        finally:
            if os.path.exists(path):
                os.remove(path)
        with open(OUT_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
        print(f"done {name} ({record['gz_mb']} MB, {record['events_total']} events, "
              f"{time.time() - started:.0f}s)", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    sys.exit(main())
