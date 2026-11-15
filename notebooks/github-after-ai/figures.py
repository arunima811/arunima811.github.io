"""Data and charts for the post "GitHub After AI". Run from the folder that holds this file."""
import csv
from collections import defaultdict
from pathlib import Path

from charts import BLUE, BLUE_LIGHT, column_chart, compact, hbar_chart, time_line_chart

DATA = Path(__file__).parent / "data"

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


def _rows(name):
    with open(DATA / name, newline="") as f:
        return list(csv.DictReader(f))


def yearly():
    return [
        {
            "year": int(r["year"]),
            "commits": float(r["est_annual_adj_commits_cap1000"]),
            "prs_merged": float(r["est_annual_adj_prs_merged"]),
            "new_repos": float(r["est_annual_adj_new_repos"]),
            "median_additions": float(r["pooled_median_additions"]),
            "hours": int(r["n_hours_commits_cap1000"]),
        }
        for r in _rows("sampled_yearly.csv")
    ]


def agent_share_monthly():
    """Share of opened PRs with any AI-agent signal. Full-data months use the exact union (agent login or agent
    branch, plus body signatures before the Oct 2025 break); archive-gap months use 2 sampled hours and take the
    largest single signal, a lower bound."""
    in_full_data = lambda m: m <= "2024-05" or m >= "2025-10"
    exact = {r["month"]: float(r["ai_login_or_branch_share_pct"]) for r in _rows("agent_prs_monthly.csv")
             if r["ai_login_or_branch_share_pct"] and in_full_data(r["month"])}
    sampled = defaultdict(float)
    for r in _rows("signature_gap_samples.csv"):
        if r["population"] == "opened" and r["signal"] in ("all_ai_agent_logins", "branch_any_agent_prefix", "sig_any_specific"):
            sampled[r["month"]] = max(sampled[r["month"]], float(r["share_pct"] or 0))
    months = sorted(set(exact) | set(sampled))
    return [{"month": m, "share": exact.get(m, sampled.get(m, 0.0)), "sampled": m not in exact} for m in months]


def agent_tools():
    months = {"2025-11", "2025-12", "2026-01", "2026-02"}
    branch = defaultdict(int)
    for r in _rows("signature_prs_monthly.csv"):
        if r["population"] == "opened" and r["month"] in months and r["signal_type"] == "head_branch_prefix":
            branch[r["signal"]] += int(float(r["matched_prs"] or 0))
    jules = sum(int(float(r["google_jules"] or 0)) for r in _rows("agent_prs_monthly.csv") if r["month"] in months)
    items = [("Codex", branch["branch_codex"]), ("Claude", branch["branch_claude"]), ("Copilot", branch["branch_copilot"]),
             ("Jules", jules), ("Cursor", branch["branch_cursor"]), ("Devin", branch["branch_devin"])]
    return sorted(items, key=lambda kv: -kv[1])


def _table(headers, rows):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f"<details><summary>Data table</summary><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></details>"


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
    pts = [{"x": str(r["year"]), "value": r["commits"], "color": BLUE,
            "tip": f"{r['year']}: about {compact(r['commits'])} public commits ({r['hours']} sampled hours)"} for r in yearly()]
    return column_chart(pts, label="Estimated public commits per year (at most 1,000 per push), 2015 to 2025", band_from="2022",
                        band_label="AI coding tools", value_labels=("2015", "2025"))


def yearly_table():
    rows = [[r["year"], compact(r["commits"]), compact(r["prs_merged"]), compact(r["new_repos"]), int(r["median_additions"])] for r in yearly()]
    return _table(["Year", "Public commits (at most 1,000 per push)", "PRs merged", "New repos", "Median lines added per merged PR"], rows)


def pr_size_chart():
    pts = [{"x": str(r["year"]), "value": r["median_additions"], "color": BLUE,
            "tip": f"{r['year']}: median merged PR adds {int(r['median_additions'])} lines"} for r in yearly()]
    return column_chart(pts, label="Median lines added per merged public PR, 2015 to 2025", fmt=lambda v: f"{v:g}",
                        band_from="2022", band_label="AI coding tools", value_labels=("2015", "2024", "2025"))


def agent_share_chart():
    series = agent_share_monthly()
    pts = [{"x": s["month"], "tick": "’" + s["month"][2:4] if s["month"].endswith("-01") else "", "value": s["share"],
            "color": BLUE_LIGHT if s["sampled"] else BLUE,
            "tip": f"{s['month']}: {s['share']:.2f}% of new PRs ({'sampled hours' if s['sampled'] else 'full data'})"} for s in series]
    return column_chart(pts, label="Share of new public PRs with an AI-agent signal, by month", fmt=lambda v: f"{v:g}%",
                        band_from="2025-05", band_label="coding agents launch", legend=[("sampled hours", BLUE_LIGHT), ("full data", BLUE)])


def agent_share_table():
    return _table(["Month", "Share of new PRs", "Source"],
                  [[s["month"], f"{s['share']:.2f}%", "sampled hours" if s["sampled"] else "full data"] for s in agent_share_monthly()])


def agent_tools_chart():
    items = [{"name": n, "value": v, "tip": f"{n}: {v:,} PRs opened, Nov 2025 to Feb 2026"} for n, v in agent_tools()]
    return hbar_chart(items, label="Public PRs opened by AI coding agents, Nov 2025 to Feb 2026")


def agent_tools_table():
    return _table(["Agent", "PRs opened (Nov 2025 to Feb 2026)"], [[n, f"{v:,}"] for n, v in agent_tools()])


# GitHub's own count of public contributions (Octoverse 2024 image alt "nearly 1 billion", 2025, 2026).
PUBLIC_CONTRIBUTIONS = [("2024", 1.0e9, "nearly 1 billion"), ("2025", 1.12e9, "1.12 billion"), ("2026", 2.5e9, "2.5 billion")]


def contributions_chart():
    pts = [{"x": y, "value": v, "color": BLUE, "tip": f"{y}: {label} public contributions"} for y, v, label in PUBLIC_CONTRIBUTIONS]
    return column_chart(pts, label="Public contributions on GitHub per year, GitHub's own count, 2024 to 2026",
                        value_labels=("2024", "2025", "2026"))


def contributions_table():
    return _table(["Year", "Public contributions"], [[y, label] for y, _, label in PUBLIC_CONTRIBUTIONS])


def agent_share_zoom_chart():
    series = [s for s in agent_share_monthly() if s["month"] >= "2024-07"]
    pts = [{"x": s["month"], "tick": s["month"][5:7] + "/" + s["month"][2:4] if s["month"][5:7] in ("01", "07") else "",
            "value": s["share"], "color": BLUE_LIGHT if s["sampled"] else BLUE,
            "tip": f"{s['month']}: {s['share']:.2f}% of new PRs ({'sampled hours' if s['sampled'] else 'full data'})"} for s in series]
    return column_chart(pts, label="Share of new public PRs with an AI-agent signal, Jul 2024 to Jun 2026", fmt=lambda v: f"{v:g}%",
                        band_from="2025-05", band_label="coding agents launch", legend=[("sampled hours", BLUE_LIGHT), ("full data", BLUE)])


def pr_size_zoom_chart():
    rows = [r for r in yearly() if r["year"] >= 2022]
    pts = [{"x": str(r["year"]), "value": r["median_additions"], "color": BLUE,
            "tip": f"{r['year']}: median merged PR adds {int(r['median_additions'])} lines"} for r in rows]
    pts.append({"x": "late 2025", "value": 35, "color": BLUE, "tip": "25 Sep to 8 Oct 2025 (full data): median merged PR adds 35 lines"})
    return column_chart(pts, label="Median lines added per merged public PR, 2022 to late 2025", fmt=lambda v: f"{v:g}",
                        value_labels=tuple(p["x"] for p in pts))
