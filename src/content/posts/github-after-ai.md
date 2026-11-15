---
title: GitHub after AI
date: 2026-11-15
tab: work
summary: What eighteen years of GitHub data say about AI and code, where the jump really is, and what nobody can measure yet.
image: /posts/github-after-ai/og.png
tags: [ai, github, data engineering]
---

I wanted to know how much AI has changed the way code gets written. GitHub is the closest thing we have to a public record of software, so I collected its numbers from 2008 to 2026, measured public activity from the GH Archive event log, and read the studies on AI and code quality. Here is what the numbers show, and where they stop.

## In short

- **The jump is real, and it landed in 2026.** In the year to September 2026, GitHub counted 34.3 billion commits and 1.3 billion merged pull requests, both more than three times the level of two years earlier. Public contributions more than doubled in a single year.
- **People didn't triple; output did.** Developers grew about 1.5 times over the same two years, so each developer ships at least twice as much.
- **Agents arrived in mid-2025.** On public repositories, AI-agent signals went from almost nothing to 5–11% of new pull requests from June 2025, and to 11–13% since November 2025. GitHub says agents started more than 40% of all pull requests by September 2026.
- **Changes got bigger.** The median merged public pull request added 22–23 lines from 2022 to 2024, 30 in 2025, and 35 in the last weeks of full data.
- **The public record went dark right before the jump.** GitHub stopped publishing commit counts and pull request sizes in its public event stream in October 2025, and most of the growth is in private repositories, so long-run public charts look flat.
- **More code is not the same as better code.** Studies find more copy/paste, much less refactoring, and mixed effects on speed and stability.

## The numbers now

<div class="stats"><div><b>225M+</b><span>developers, 2026</span></div><div><b>34.3B</b><span>commits in the year to Sep 2026</span></div><div><b>1.3B</b><span>pull requests merged, same year</span></div><div><b>3×</b><span>commits and merged PRs vs two years earlier</span></div><div><b>40%+</b><span>of pull requests started by an agent, Sep 2026</span></div></div>

Sources: [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/) and [Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/). The 2026 figures include public and private repositories.

## 2026 is the jump

GitHub's own count of public contributions grew 12% from 2024 to 2025, then more than doubled in 2026. Across all repositories the jump is bigger: commits and merged pull requests both more than tripled in two years.

![Public contributions on GitHub per year, GitHub&#x27;s own count, 2024 to 2026](/posts/github-after-ai/contributions.svg)

<details><summary>Data table</summary><table><thead><tr><th>Year</th><th>Public contributions</th></tr></thead><tbody><tr><td>2024</td><td>nearly 1 billion</td></tr><tr><td>2025</td><td>1.12 billion</td></tr><tr><td>2026</td><td>2.5 billion</td></tr></tbody></table></details>

## Agents arrived in mid-2025

I looked for AI-agent fingerprints on new public pull requests: pull requests opened by agent accounts such as Copilot or Jules, branches named the way agents name them (`codex/`, `claude/`, `copilot/`, `cursor/`, `devin/`), and, while GitHub still published them, AI-tool links in the description.

![Share of new public PRs with an AI-agent signal, Jul 2024 to Jun 2026](/posts/github-after-ai/agent_share_zoom.svg)

<details><summary>Data table</summary><table><thead><tr><th>Month</th><th>Share of new PRs</th><th>Source</th></tr></thead><tbody><tr><td>2023-02</td><td>0.00%</td><td>full data</td></tr><tr><td>2023-03</td><td>0.00%</td><td>full data</td></tr><tr><td>2023-04</td><td>0.00%</td><td>full data</td></tr><tr><td>2023-05</td><td>0.00%</td><td>full data</td></tr><tr><td>2023-06</td><td>0.02%</td><td>full data</td></tr><tr><td>2023-07</td><td>0.06%</td><td>full data</td></tr><tr><td>2023-08</td><td>0.07%</td><td>full data</td></tr><tr><td>2023-09</td><td>0.03%</td><td>full data</td></tr><tr><td>2023-10</td><td>0.03%</td><td>full data</td></tr><tr><td>2023-11</td><td>0.03%</td><td>full data</td></tr><tr><td>2023-12</td><td>0.06%</td><td>full data</td></tr><tr><td>2024-01</td><td>0.26%</td><td>full data</td></tr><tr><td>2024-02</td><td>0.03%</td><td>full data</td></tr><tr><td>2024-03</td><td>0.04%</td><td>full data</td></tr><tr><td>2024-04</td><td>0.02%</td><td>full data</td></tr><tr><td>2024-05</td><td>0.02%</td><td>full data</td></tr><tr><td>2024-06</td><td>0.04%</td><td>sampled hours</td></tr><tr><td>2024-07</td><td>0.01%</td><td>sampled hours</td></tr><tr><td>2024-08</td><td>0.01%</td><td>sampled hours</td></tr><tr><td>2024-09</td><td>0.00%</td><td>sampled hours</td></tr><tr><td>2024-10</td><td>0.00%</td><td>sampled hours</td></tr><tr><td>2024-11</td><td>0.03%</td><td>sampled hours</td></tr><tr><td>2024-12</td><td>0.08%</td><td>sampled hours</td></tr><tr><td>2025-01</td><td>0.03%</td><td>sampled hours</td></tr><tr><td>2025-02</td><td>0.08%</td><td>sampled hours</td></tr><tr><td>2025-03</td><td>0.14%</td><td>sampled hours</td></tr><tr><td>2025-04</td><td>0.16%</td><td>sampled hours</td></tr><tr><td>2025-05</td><td>0.08%</td><td>sampled hours</td></tr><tr><td>2025-06</td><td>11.15%</td><td>sampled hours</td></tr><tr><td>2025-07</td><td>5.50%</td><td>sampled hours</td></tr><tr><td>2025-08</td><td>9.84%</td><td>sampled hours</td></tr><tr><td>2025-09</td><td>5.58%</td><td>sampled hours</td></tr><tr><td>2025-10</td><td>9.63%</td><td>full data</td></tr><tr><td>2025-11</td><td>12.47%</td><td>full data</td></tr><tr><td>2025-12</td><td>10.89%</td><td>full data</td></tr><tr><td>2026-01</td><td>10.95%</td><td>full data</td></tr><tr><td>2026-02</td><td>11.99%</td><td>full data</td></tr><tr><td>2026-03</td><td>12.70%</td><td>full data</td></tr><tr><td>2026-04</td><td>11.55%</td><td>full data</td></tr><tr><td>2026-05</td><td>12.79%</td><td>full data</td></tr><tr><td>2026-06</td><td>12.01%</td><td>full data</td></tr></tbody></table></details>

The signal stayed under 0.3% of new pull requests in every month until May 2025. From June 2025 it jumped to between 5 and 11%, right after OpenAI Codex, the Copilot coding agent, Google Jules and Claude Code all launched in May. Since November 2025 it has held at 11 to 13%. These are lower bounds: help from an assistant inside an editor leaves no public trace.

![Public PRs opened by AI coding agents, Nov 2025 to Feb 2026](/posts/github-after-ai/agent_tools.svg)

<details><summary>Data table</summary><table><thead><tr><th>Agent</th><th>PRs opened (Nov 2025 to Feb 2026)</th></tr></thead><tbody><tr><td>Codex</td><td>500,930</td></tr><tr><td>Claude</td><td>433,742</td></tr><tr><td>Copilot</td><td>329,187</td></tr><tr><td>Jules</td><td>100,053</td></tr><tr><td>Cursor</td><td>34,292</td></tr><tr><td>Devin</td><td>12,361</td></tr></tbody></table></details>

From November 2025 to February 2026, Codex opened the most public pull requests, followed by Claude and Copilot.

## Changes got bigger

Lines of code is the number I most wanted, and nobody publishes it. The closest public measure is the size of merged pull requests. The typical merged pull request added 22 or 23 lines from 2022 to 2024. In 2025 it added 30, and in the last two weeks of full data (25 September to 8 October 2025) the median was 35.

![Median lines added per merged public PR, 2022 to late 2025](/posts/github-after-ai/pr_size_zoom.svg)

That fits how agents work: GitHub found that agent-started pull requests change several files 87% of the time, against 79% for the rest. For ten years before that, from 2015 to 2024, the median never left the 18–26 line range (data table below).

## Why the long-run public charts look flat

I also measured public activity directly from [GH Archive](https://www.gharchive.org/), the public log of GitHub events. Merged pull requests grew 35% a year from 2015 to 2022, and 8% a year from 2022 to 2025. Public commits grew about 27% a year before and 12% a year after, counting at most 1,000 commits per push: GitHub raised its own per-push cap from 1,000 to 10,000 in June 2023, and the cap keeps the years comparable. Counting every commit gives about 28% a year after 2022, and the difference comes entirely from very large pushes of more than 1,000 commits.

![Estimated public commits per year (at most 1,000 per push), 2015 to 2025](/posts/github-after-ai/commits.svg)

<details><summary>Data table</summary><table><thead><tr><th>Year</th><th>Public commits (at most 1,000 per push)</th><th>PRs merged</th><th>New repos</th><th>Median lines added per merged PR</th></tr></thead><tbody><tr><td>2015</td><td>406.2M</td><td>4M</td><td>11.4M</td><td>21</td></tr><tr><td>2016</td><td>616.6M</td><td>8M</td><td>15.7M</td><td>18</td></tr><tr><td>2017</td><td>797M</td><td>11.4M</td><td>22.3M</td><td>24</td></tr><tr><td>2018</td><td>884.1M</td><td>13M</td><td>23M</td><td>23</td></tr><tr><td>2019</td><td>1.2B</td><td>19.1M</td><td>27.9M</td><td>25</td></tr><tr><td>2020</td><td>1.2B</td><td>23.7M</td><td>35.7M</td><td>26</td></tr><tr><td>2021</td><td>1.6B</td><td>32.9M</td><td>58.4M</td><td>24</td></tr><tr><td>2022</td><td>2.1B</td><td>33.2M</td><td>56.2M</td><td>22</td></tr><tr><td>2023</td><td>2.4B</td><td>38.5M</td><td>58.4M</td><td>22</td></tr><tr><td>2024</td><td>2.9B</td><td>41.5M</td><td>66M</td><td>23</td></tr><tr><td>2025</td><td>3B</td><td>41.8M</td><td>63.4M</td><td>30</td></tr></tbody></table></details>

So the public record shows steady growth through 2025, not an explosion. Three things explain the gap with GitHub's numbers. Most work is private: 81.5% of contributions were in private repositories already in 2025. The big jump came in 2026. And in October 2025 GitHub stopped publishing commit counts in its public event stream, so the public log can't see the jump at all.

## Eighteen years of growth

For context: GitHub's growth in people kept its shape through the AI era. From 2012 on, developers roughly doubled every two to three years.

![GitHub developers, millions, 2008 to 2026](/posts/github-after-ai/developers.svg)

<details><summary>Data table</summary><table><thead><tr><th>As of</th><th>Developers</th></tr></thead><tbody><tr><td>end of 2008</td><td>40K</td></tr><tr><td>Jul 2009</td><td>100K</td></tr><tr><td>Sep 2011</td><td>1M</td></tr><tr><td>Dec 2012</td><td>2.8M</td></tr><tr><td>Dec 2013</td><td>4M</td></tr><tr><td>2017</td><td>24M</td></tr><tr><td>2018</td><td>31M</td></tr><tr><td>2019</td><td>40M</td></tr><tr><td>2020</td><td>56M</td></tr><tr><td>2021</td><td>73M</td></tr><tr><td>2022</td><td>94M</td></tr><tr><td>Jan 2023</td><td>100M</td></tr><tr><td>Dec 2024</td><td>150M</td></tr><tr><td>Aug 2025</td><td>180M</td></tr><tr><td>Sep 2026</td><td>225M</td></tr></tbody></table></details>

![GitHub repositories, millions, 2009 to 2025](/posts/github-after-ai/repositories.svg)

<details><summary>Data table</summary><table><thead><tr><th>As of</th><th>Repositories</th></tr></thead><tbody><tr><td>Jan 2009, public only</td><td>50K</td></tr><tr><td>Jul 2010</td><td>1M</td></tr><tr><td>Dec 2012</td><td>4.6M</td></tr><tr><td>Dec 2013</td><td>10M</td></tr><tr><td>2017</td><td>67M</td></tr><tr><td>Nov 2018</td><td>100M</td></tr><tr><td>2023</td><td>420M</td></tr><tr><td>2024</td><td>518M</td></tr><tr><td>Aug 2025</td><td>630M</td></tr></tbody></table></details>

GitHub has changed what it counts over the years (public only, all repositories, with or without forks), so read these as the numbers GitHub reported at the time.

## More code, same quality?

- **Code quality.** [GitClear](https://www.gitclear.com/ai_assistant_code_quality_2025_research) (211 million changed lines, 2020–2024): refactored, "moved" code fell from 25% of changed lines in 2021 to under 10% in 2024, while copy/pasted lines rose from 8.3% to 12.3%. Its [2026 report](https://www.gitclear.com/the_ai_code_quality_maintainability_gap) puts moved code at 3.8% and copy/paste at 15.7% in the first half of 2026.
- **Speed.** In [METR's 2025 trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), 16 experienced open-source developers took 19% longer on 246 real tasks with AI tools, while believing they were 20% faster. A [2026 follow-up](https://metr.org/blog/2026-02-24-uplift-update/) could not get a clean answer, partly because developers no longer want to work without AI.
- **Delivery.** In [DORA 2024](https://services.google.com/fh/files/misc/2024_final_dora_report.pdf), more AI adoption came with slightly lower throughput and lower stability. In [DORA 2025](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf), throughput improved, but instability still rose.
- **Trust.** In the [Stack Overflow survey](https://survey.stackoverflow.co/2025/ai), AI tool use went from 70% of developers in 2023 to 84% in 2025, while 46% distrusted the accuracy of AI tools and 33% trusted it.
- **Inside companies.** Google said more than a quarter of its new code was AI-generated in [October 2024](https://blog.google/inside-google/message-ceo/alphabet-earnings-q3-2024/), and 75% in [April 2026](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/cloud-next-2026-sundar-pichai/). Microsoft said 20–30% in [April 2025](https://www.cnbc.com/2025/04/29/satya-nadella-says-as-much-as-30percent-of-microsoft-code-is-written-by-ai.html).

## What we can't measure

- **Lines of code.** GitHub reports pushes, commits, pull requests and contributions, never lines. The closest large count is [Software Heritage](https://www.softwareheritage.org/2026/01/21/software-heritage-archive-digital-public-good/)'s 27 billion unique source files across all code hosts, and that counts files, not lines.
- **Private code.** Most work happens in private repositories, which public data can't see.
- **The public record after October 2025.** GitHub [removed commit counts, pull request sizes and descriptions](https://github.blog/changelog/2025-08-08-upcoming-changes-to-github-events-api-payloads/) from its public event stream on 7 October 2025. Google's open source team [estimates](https://opensource.googleblog.com/2026/09/how-much-should-you-trust-your-oss-data.html) GH Archive now captures about half of events, and as little as 20% for some types.
- **Comparisons across GitHub reports.** Octoverse 2025 counted public activity only, and Octoverse 2026 counts public and private repositories, so their totals can't be compared directly.

## Reproduce it

Everything here comes from public data. The [analysis notebook, data, queries and scripts](https://github.com/arunima811/arunima811.github.io/tree/main/notebooks/github-after-ai) are in this site's repository.

- **2023 to mid-2026, exact counts:** the GH Archive mirror on the free [ClickHouse playground](https://play.clickhouse.com/) (table `github_events`). It has no data from June 2024 to late September 2025. `queries.sql` holds the final queries.
- **2015 to 2025, yearly estimates:** four sampled hours per year from the raw GH Archive files (`scripts/sample_gharchive.py`), scaled to a year with weekday and weekend factors. On full 2023 data this lands within 1 to 9% of the exact totals. The 2015–2019 levels are probably overstated, so growth before AI is if anything understated.
- **Archive-gap months for the agent charts:** two sampled hours per month (`scripts/sample_signatures.py`).

This snippet rebuilds the monthly agent-branch share straight from the playground (about a second):

```python
import urllib.request

SQL = """
SELECT
    toStartOfMonth(created_at) AS month,
    count() AS prs_opened,
    countIf(startsWith(lower(head_ref), 'claude/')) AS branch_claude,
    countIf(startsWith(lower(head_ref), 'codex/')) AS branch_codex,
    countIf(startsWith(lower(head_ref), 'copilot/')) AS branch_copilot,
    countIf(startsWith(lower(head_ref), 'cursor/')) AS branch_cursor,
    countIf(startsWith(lower(head_ref), 'devin/')) AS branch_devin,
    countIf(multiSearchAny(lower(head_ref), ['claude/', 'codex/', 'copilot/', 'cursor/', 'devin/']) AND match(lower(head_ref), '^(claude|codex|copilot|cursor|devin)/')) AS branch_any_agent_prefix
FROM github_events
WHERE event_type = 'PullRequestEvent' AND action = 'opened'
  AND created_at >= '2023-02-01 00:00:00' AND created_at < '2026-07-01 00:00:00'
GROUP BY month
ORDER BY month FORMAT CSVWithNames;
"""
req = urllib.request.Request("https://play.clickhouse.com/?user=play", data=(SQL.strip().rstrip(";") + " FORMAT TSVWithNames").encode())
print(urllib.request.urlopen(req, timeout=120).read().decode())
```

GitHub's own numbers (developers, repositories, the 2026 totals) come from GitHub's blog and Octoverse reports, linked above. GitHub has changed its definitions several times, so treat cross-year comparisons of those as approximate.
