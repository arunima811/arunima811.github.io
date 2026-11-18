"""Data and charts for the post "GitHub After AI". Run from the folder that holds this file."""
import csv
from html import escape
from pathlib import Path

from charts import AQUA, BLUE, BLUE_LIGHT, GRAY, ORANGE, column_chart, compact, hbar_chart, stacked_columns, time_line_chart

DATA = Path(__file__).parent / "data"
MONTH_NAMES = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

# GitHub's own published milestones: (decimal year, millions, as of, source key). See the post's sources list.
DEVELOPERS = [
    (2008.99, 0.04, "end of 2008", "blog-2009"), (2009.51, 0.1, "Jul 2009", "blog-100k"),
    (2011.71, 1, "Sep 2011", "blog-3m"), (2012.97, 2.8, "Dec 2012", "octo-2012"),
    (2013.97, 4, "Dec 2013", "about-2013"), (2017.75, 24, "2017", "octo-2017"),
    (2018.75, 31, "2018", "octo-2018"), (2019.75, 40, "2019", "octo-2019"),
    (2020.75, 56, "2020", "octo-2020"), (2021.75, 73, "2021", "octo-2021"),
    (2022.75, 94, "2022", "octo-2022"), (2023.07, 100, "Jan 2023", "blog-100m"),
    (2024.96, 150, "Dec 2024", "blog-150m"), (2025.66, 180, "Aug 2025", "octo-2025"),
    (2026.75, 225, "Sep 2026", "octo-2026"),
]
REPOSITORIES = [
    (2009.0, 0.05, "Jan 2009, public only", "blog-2009"), (2010.56, 1, "Jul 2010", "blog-1m-repos"),
    (2012.97, 4.6, "Dec 2012", "octo-2012"), (2013.97, 10, "Dec 2013", "blog-10m-repos"),
    (2017.75, 67, "2017", "octo-2017"), (2018.85, 100, "Nov 2018", "blog-100m-repos"),
    (2023.75, 420, "2023", "octo-2023"), (2024.75, 518, "2024", "octo-2024"), (2025.66, 630, "Aug 2025", "octo-2025"),
]
LAST_GH_ARCHIVE_YEAR = 2024
AGENT_MONTHS_FROM = "2025-01"


def _rows(name):
    with open(DATA / name, newline="") as f:
        return list(csv.DictReader(f))


def _month_label(month):
    return f"{MONTH_NAMES[int(month[5:7]) - 1]} {month[:4]}"


def _pct(v):
    return "<0.001%" if 0 < v < 0.001 else f"{v:.3g}%"


def _table(headers, rows):
    head = "".join(f"<th>{escape(str(h))}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{escape(str(c))}</td>" for c in row) + "</tr>" for row in rows)
    return f"<details><summary>Data table</summary><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></details>"


# GH Archive sampled hours, 2015 onward (data/sampled_yearly.csv).
def yearly():
    return [
        {
            "year": int(r["year"]),
            "commits": float(r["est_annual_adj_commits_cap1000"]),
            "prs_merged": float(r["est_annual_adj_prs_merged"]),
            "median_additions": float(r["pooled_median_additions"]),
            "hours": int(r["n_hours_commits_cap1000"]),
        }
        for r in _rows("sampled_yearly.csv")
    ]


# GitHub Search API counts, one row per month from 2022-01 (data/api/monthly.csv).
def api_monthly():
    return [{k: (v if k == "month" or k.endswith("_flag") else int(v) if v else None) for k, v in r.items()}
            for r in _rows("api/monthly.csv")]


def api_yearly():
    """Merged PRs per month (average) and new repos per year; the last year is partial, compared with the same months a year before."""
    months = api_monthly()
    by_year = {}
    for m in months:
        by_year.setdefault(int(m["month"][:4]), []).append(m)
    out = []
    for year, ms in sorted(by_year.items()):
        prev = [m for m in by_year.get(year - 1, []) if m["month"][5:] <= ms[-1]["month"][5:]]
        merged, repos = sum(m["merged_prs"] for m in ms), sum(m["new_repos"] for m in ms)
        out.append({
            "year": year, "months": len(ms), "last": ms[-1]["month"],
            "merged_per_month": merged / len(ms), "new_repos": repos,
            "merged_change": merged / sum(m["merged_prs"] for m in prev) - 1 if prev else None,
            "repos_change": repos / sum(m["new_repos"] for m in prev) - 1 if prev else None,
        })
    return out


def agent_signals():
    """Share of opened PRs carrying each AI-tool signal. Codex is the larger of its body link and `codex/` branches
    (the link stopped in Nov 2025); Cursor is the larger of its two body links, which mostly overlap."""
    out = []
    for m in api_monthly():
        if m["month"] < AGENT_MONTHS_FROM:
            continue
        counts = {
            "Claude Code": m["claude_code"],
            "Codex": max(m["codex"], m["branch_codex"] or 0),
            "Copilot agent": m["copilot_agent"],
            "Cursor": max(m["cursor_agents"], m["cursor_background_agent"]),
            "Devin and Jules": m["devin"] + m["jules"],
        }
        out.append({"month": m["month"], "opened": m["opened_prs"], "counts": counts,
                    "shares": {k: 100 * v / m["opened_prs"] for k, v in counts.items()},
                    "total_share": 100 * sum(counts.values()) / m["opened_prs"]})
    return out


def validation():
    rows = []
    for r in _rows("api/validation_vs_gharchive.csv"):
        if " " in r["month"]:
            continue
        if r["ratio_merged_gha_over_search"]:
            rows.append((r["month"], "merged", int(r["gha_prs_merged_fixed"]), int(r["search_merged_prs"]), float(r["ratio_merged_gha_over_search"])))
        else:
            rows.append((r["month"], "opened", int(r["gha_prs_opened"]), int(r["search_opened_prs"]), float(r["ratio_opened_gha_over_search"])))
    return rows


def developers_chart():
    pts = [{"x": x, "value": v, "tip": f"{when}: {compact(v * 1e6)} developers"} for x, v, when, _ in DEVELOPERS]
    return time_line_chart(pts, label="GitHub developers, millions, 2008 to 2026", fmt=lambda v: f"{v:g}M" if v else "0",
                           x_ticks=[2008, 2011, 2014, 2017, 2020, 2023, 2026], band_from=2022.47, band_label="AI coding tools")


def developers_table():
    return _table(["As of", "Developers"], [[w, f"{compact(v * 1e6)}"] for _, v, w, _ in DEVELOPERS])


def repositories_chart():
    pts = [{"x": x, "value": v, "tip": f"{when}: {compact(v * 1e6)} repositories"} for x, v, when, _ in REPOSITORIES]
    return time_line_chart(pts, label="GitHub repositories, millions, 2009 to 2025", fmt=lambda v: f"{v:g}M" if v else "0",
                           x_ticks=[2008, 2011, 2014, 2017, 2020, 2023, 2026], band_from=2022.47, band_label="AI coding tools")


def repositories_table():
    return _table(["As of", "Repositories"], [[w, compact(v * 1e6)] for _, v, w, _ in REPOSITORIES])


def commits_chart():
    rows = [r for r in yearly() if r["year"] <= LAST_GH_ARCHIVE_YEAR]
    pts = [{"x": str(r["year"]), "value": r["commits"], "color": BLUE,
            "tip": f"{r['year']}: about {compact(r['commits'])} public commits ({r['hours']} sampled hours)"} for r in rows]
    return column_chart(pts, label=f"Estimated public commits per year (at most 1,000 per push), 2015 to {LAST_GH_ARCHIVE_YEAR}",
                        band_from="2022", band_label="AI coding tools", value_labels=("2015", str(LAST_GH_ARCHIVE_YEAR)))


def commits_table():
    search = {y["year"]: y["merged_per_month"] * y["months"] for y in api_yearly()}
    rows = [[r["year"], compact(r["commits"]), compact(r["prs_merged"]), compact(search[r["year"]]) if r["year"] in search else ""]
            for r in yearly() if r["year"] <= LAST_GH_ARCHIVE_YEAR]
    return _table(["Year", "Public commits (at most 1,000 per push)", "Merged PRs (GH Archive)", "Merged PRs (Search API)"], rows)


def merged_monthly_chart():
    pts = [{"x": m["month"], "tick": m["month"][:4] if m["month"].endswith("-01") else "", "value": m["merged_prs"], "color": BLUE,
            "tip": f"{_month_label(m['month'])}: {m['merged_prs']:,} public PRs merged"} for m in api_monthly()]
    return column_chart(pts, label="Public pull requests merged per month, January 2022 to October 2026",
                        band_from="2025-05", band_label="agents widely available", value_labels=("2022-01", "2025-05", pts[-1]["x"]))


def merged_monthly_table():
    return _table(["Month", "Public PRs merged"], [[_month_label(m["month"]), f"{m['merged_prs']:,}"] for m in api_monthly()])


def merged_yearly_html():
    rows = []
    for y in api_yearly():
        partial = y["months"] < 12
        year = f"{y['year']} (Jan to {MONTH_NAMES[int(y['last'][5:]) - 1]})" if partial else str(y["year"])
        change = "" if y["merged_change"] is None else f"{y['merged_change']:+.0%}" + (" vs same months" if partial else "")
        rows.append(f"<tr><td>{year}</td><td>{y['merged_per_month'] / 1e6:.2f}M</td><td>{change}</td></tr>")
    return ("<table><thead><tr><th>Year</th><th>Public PRs merged per month</th><th>Change</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def new_repos_chart():
    pts = []
    for y in api_yearly():
        partial = y["months"] < 12
        pts.append({"x": str(y["year"]), "tick": f"Jan–{MONTH_NAMES[int(y['last'][5:]) - 1]} {y['year']}" if partial else str(y["year"]),
                    "value": y["new_repos"], "color": BLUE_LIGHT if partial else BLUE,
                    "tip": f"{y['year']}{' (January to ' + MONTH_NAMES[int(y['last'][5:]) - 1] + ' only)' if partial else ''}: "
                           f"{y['new_repos']:,} new public repositories (not forks)"})
    return column_chart(pts, label="New public repositories per year (not forks), 2022 to October 2026",
                        value_labels=tuple(p["x"] for p in pts), legend=[("full year", BLUE), ("year so far", BLUE_LIGHT)])


def new_repos_table():
    rows = [[f"{y['year']}" + (" (Jan to Oct)" if y["months"] < 12 else ""), f"{y['new_repos']:,}",
             "" if y["repos_change"] is None else f"{y['repos_change']:+.0%}" + (" vs same months" if y["months"] < 12 else "")]
            for y in api_yearly()]
    return _table(["Year", "New public repositories", "Change"], rows)


AGENT_SERIES = [("Claude Code", ORANGE), ("Codex", BLUE), ("Copilot agent", AQUA), ("Cursor", BLUE_LIGHT), ("Devin and Jules", GRAY)]


def agent_share_chart():
    signals = agent_signals()
    labels = [f"{MONTH_NAMES[int(s['month'][5:]) - 1]} ’{s['month'][2:4]}" for s in signals]
    series = [(name, color, [s["shares"][name] for s in signals]) for name, color in AGENT_SERIES]
    return stacked_columns(labels, series, label="Share of new public pull requests with an AI-tool signal, by tool, January 2025 to October 2026",
                           fmt=_pct, tick_every=3)


def agent_share_table():
    names = [n for n, _ in AGENT_SERIES]
    rows = [[_month_label(s["month"]), f"{s['opened']:,}"] + [_pct(s["shares"][n]) for n in names] + [_pct(s["total_share"])] for s in agent_signals()]
    return _table(["Month", "New public PRs"] + names + ["All signals"], rows)


def agent_tools_chart():
    last = agent_signals()[-1]
    when = _month_label(last["month"])
    items = sorted(({"name": n, "value": v, "tip": f"{n}: {v:,} public PRs opened in {when} ({_pct(last['shares'][n])} of all)"}
                    for n, v in last["counts"].items()), key=lambda i: -i["value"])
    return hbar_chart(items, label=f"Public pull requests opened with each tool's signal, {when}")


def agent_tools_table():
    last = agent_signals()[-1]
    rows = [[n, f"{v:,}", _pct(last["shares"][n])] for n, v in sorted(last["counts"].items(), key=lambda kv: -kv[1])]
    return _table(["Tool", f"Public PRs opened, {_month_label(last['month'])}", "Share of all new PRs"], rows)


def pr_size_zoom_chart():
    rows = [r for r in yearly() if r["year"] >= 2022]
    pts = [{"x": str(r["year"]), "value": r["median_additions"], "color": BLUE,
            "tip": f"{r['year']}: median merged PR adds {int(r['median_additions'])} lines"} for r in rows]
    pts.append({"x": "late 2025", "value": 35, "color": BLUE, "tip": "25 Sep to 8 Oct 2025 (full data): median merged PR adds 35 lines"})
    return column_chart(pts, label="Median lines added per merged public PR, 2022 to late 2025", fmt=lambda v: f"{v:g}",
                        value_labels=tuple(p["x"] for p in pts))


def pr_size_table():
    rows = [[r["year"], int(r["median_additions"])] for r in yearly()] + [["25 Sep to 8 Oct 2025", 35]]
    return _table(["Year", "Median lines added per merged public PR"], rows)


def validation_table():
    rows = [[_month_label(m), kind, f"{gha:,}", f"{search:,}", f"{ratio:.2f}"] for m, kind, gha, search, ratio in validation()]
    return _table(["Month", "Public PRs", "GH Archive", "Search API", "GH Archive ÷ Search"], rows)
