# GitHub activity and AI-agent data pull (public GH Archive data)

Pulled 2026-11-15. Public data only:

- **Source A**: the ClickHouse public playground table `github_events`, a mirror of GH Archive.
- **Source B**: raw GH Archive hourly files from `data.gharchive.org`.

No GitHub token or GitHub API was used, and nothing was written to any remote service. Every SQL statement is in `queries.sql`.

## Headline summary

1. **Commits** (push size capped at 1,000 per push; Source B samples, day-type adjusted): 0.41B in 2015, 1.24B in 2019, 2.12B in 2022, 2.35B in 2023, 2.92B in 2024 and 2.97B in 2025\*.
2. **PRs merged**: 4.0M in 2015, 19.1M in 2019, 33.2M in 2022, 38.5M in 2023, 41.5M in 2024 and 41.8M in 2025\*. For comparison, the playground's true 2023 count for Feb–Dec is 33.8M, which scales to about 37.0M for 12 months.
3. **New repos**: 11.4M in 2015, 27.9M in 2019, 56.2M in 2022, 58.4M in 2023, 66.0M in 2024 and 63.4M in 2025\*. New repos cannot be measured after 2025-10-08, because GitHub stopped emitting repository CreateEvents.
4. **Median merged-PR size** (lines added): 21 in 2015, 25 in 2019, 22 in 2022, 22 in 2023 (exact), 21 in 2024 H1 (exact) and 30 in 2025\*. On full data for 2025-09-25..10-08 the exact median is 35.
5. **PRs opened by AI-agent accounts** (setup PRs excluded): 0.025% of opened PRs in 2023, about 1.1k a month, mostly Sweep. In Nov 2025–Feb 2026 this was 3.7%, about 116k a month. The Copilot coding agent alone opened about 80k a month.
6. **Any AI signal** (an agent account, or a branch starting `claude/`, `codex/`, `copilot/`, `cursor/` or `devin/`): 0.025% of opened PRs in 2023, against 11.6% in Nov 2025–Feb 2026. The share stays between 11% and 13% every month through Jun 2026.
7. **AI signatures in PR bodies** (opened PRs): 0% from 2023 to mid-2024. In the gap samples they are under 0.2% until May 2025, then 5–11% from Jun to Sep 2025. On full data for 2025-09-25..10-08 they reach 7.8–8.1%. Codex task links are 6.6%, Claude Code mentions 0.5–0.6% and Cursor agent links 0.5–0.6%.
8. **Signatures on merged PRs** run higher in the same window: 9.7–10.3%, of which Codex links are 8.2–8.9%. PR bodies are empty for every PR after 2025-10-08 17:00 UTC.
9. **Validation**: the specified estimator (mean of 4 hours × hours in the year) overstates 2023 totals by 10% (pushes) to 45% (merged PRs), because 15:00 UTC on a weekday is a busy hour. The day-type-adjusted estimator is within −9% to −1% in 2023, using factors calibrated outside 2023.
10. **2015–2019 adjusted levels are probably overstated** by about 2–36%, depending on the metric, because 15:00 UTC was a relatively busier hour then (single-day checks). Growth multiples since 2015 are therefore conservative.

\*2025 commits, merges, repos and sizes use 3 sample hours (Feb 15 Sat, May 15 Thu, Aug 15 Fri). The Nov 15 file already has the reduced payload. Push and PR-opened counts for 2025 use all 4 hours.

## Read this first: corrections to the brief

- **The playground is not continuous.** Its minimum and maximum timestamps are 2023-01-13 13:00 and 2026-07-02 22:59, as stated in the brief. But it has no rows from 2024-06-05 09:00 to 2025-09-25 21:59 UTC, a 477-day hole.
  - Raw GH Archive does have those hours. Source B samples were therefore extended to 2023–2025, and the gap was sampled for the AI signatures.
  - As a result, A1 has no full year for 2024 or 2025, and the validation could not use true 2024 or 2025 totals. Substitute windows are used instead (see Validation).
- **The 2025 field break is one event.** At 2025-10-08 17:00 UTC GitHub's Events API payload shrank, and this is visible in the raw files as well as the playground.
  - PushEvent keeps only `repository_id, push_id, ref, head, before`.
  - `pull_request` keeps only `url, id, number, head, base`.
  - Repository and tag CreateEvents disappear.
- **The playground's `merged` column breaks earlier**, at 2024-01-07 19:00, but only in the playground. Raw files still carry `pull_request.merged=true`. `merged_at` is still populated and matches the raw files exactly, so it is used for merged PRs.

## Known breaks (exclude these)

| Series | First affected month | Exact UTC | What happens | Use instead |
|---|---|---|---|---|
| `merged` flag (playground) | 2024-01 (18% set); all 0 from 2024-02 | 2024-01-07 19:00 | `merged=0` for every closed PR. Raw 2024-02-15 15:00 has 6,984 merged, which equals the playground's `merged_at` count | `prs_merged_fixed` (closed with `merged_at` set). It equals `merged=1` in every month before the break |
| commits: cap change | 2023-06 | 2023-06-30 14:39 | Per-push `push_size` cap rises from 1,000 to 10,000, which is also in the raw files. `commits` rises from 170–225M to 300–360M a month | `commits_cap1000` or `commits_lt1000` |
| commits: anomaly | 2024-04, 2024-05 | 2024-04-16 19:00 to 2024-05-06 19:00 | 30–80k pushes a day report 1,000 or more commits (normally about 1k a day), across dependabot, github-actions, renovate and the merge queue. Commits per push rise from 3–4 to 100–160 | Exclude. These cells are blank in `monthly.csv` |
| `push_size`, `push_distinct_size` | 2025-10 (69% zero), all zero from 2025-11 | 2025-10-08 17:00 | 0 for 100% of pushes | None. Commits cannot be measured after this |
| PR additions, deletions, changed_files, title, body, author, `merged_at` | 2025-10 (61–70% empty), all empty from 2025-11 | 2025-10-08 17:00 | Empty or 0 for 100% of PRs | Branch names (`head_ref`) and actor logins survive |
| Merged PRs | 2025-10 | 2025-10-08 17:00 to 2025-12-02 20:43 | No merge events at all. After that, merges appear as `action='merged'` with no sizes: about 2.2M a month, against about 3.4M before the gap | `prs_merged_action`, a different definition whose level is not comparable |
| New repos | 2025-10 | 2025-10-08 17:00 | Only `ref_type='branch'` CreateEvents remain, in raw files too | None |
| Collection outage | 2025-10 | 2025-10-08 17:00 to about 2025-10-14 | 15–19k events a day instead of about 3.5M | Treat 2025-10 as partial |
| PR, issue and watch volumes | 2026-03 | Week of 2026-03-02 | PRs opened per push fall from 0.044 (Feb) to 0.005 (Jun), and watches and issue comments fall similarly while pushes rise. The raw 2026-05-15 15:00 file shows the same drop | Do not use PR counts after 2026-02. Shares are flagged `decaying` |

Normal baselines, which are not breaks:

- Pushes with `push_size=0`: 0.1–0.3%. This was 2.8–3.1% in Feb–Mar 2023 and 1.9% during the Apr 2024 anomaly.
- Merged PRs with 0 additions and 0 deletions: 1.7–1.9%.
- Opened PRs with an empty body: 29–35%, and 21% in late Sep 2025.
- `distinct_commits` has no cap, so a few pushes of about 1M commits dominate it. Do not use it as an activity measure.

## Coverage

- **Playground**: 2023-01-13 13:00 to 2024-06-05 08:59, and 2025-09-25 22:00 to 2026-07-02 22:59 UTC.
  - `monthly.csv` covers 2023-02..2026-06, with `coverage_status` of `full`, `minor_gaps`, `partial` or `none`. A low-volume hour is one with fewer than 25% of that month's median hourly events.
  - Missing or low hours: 19 in 2023-03, 8 in 2023-11 and 9 in 2026-06. The partial months are 2024-06 (14.6% of hours), 2025-09 (16.9%) and 2025-10 (80.1%).
- **Source B**: 46 raw hours, 2.7 GB compressed, processed one file at a time and deleted after use.
  - 32 baseline hours (2015–2022).
  - 12 extension hours (2023–2025), added because of the gap.
  - 2 diagnostic hours (2026-02-15 and 2026-05-15).
  - All are on the 15th of Feb, May, Aug and Nov at 15:00 UTC.
- **Gap samples**: 32 raw hours on the 15th of every month from 2024-06 to 2025-09, at 03:00 and 15:00 UTC.
- **Weekend sample days**: in 2015 Feb, Aug and Nov; in 2016 May; in 2020 Feb, Aug and Nov; in 2021 May and Aug; in 2022 May; and in 2025 Feb and Nov. 2017–2019, 2023 and 2024 have no weekend samples.

## Files and columns

**`monthly.csv` (A1)** has one row per month, 2023-02..2026-06. Cells known to be broken are blank, and the reason is in `notes`. The unblanked query output is in `work/monthly_raw.csv`.

- Coverage columns:
  - `coverage_status`, `coverage_pct`, `hours_with_data`, `low_volume_hours` and `hours_in_month` describe coverage.
- Push columns:
  - `push_events`: count of PushEvents.
  - `commits`: sum of `push_size`.
  - `distinct_commits`: sum of `push_distinct_size`.
  - `commits_cap1000`: sum of min(size, 1000).
  - `commits_lt1000`: commits in pushes of under 1,000 commits.
  - `pushes_ge_1000`: pushes of 1,000 commits or more.
  - `pushers`: approximate count of distinct actors on PushEvents, using `uniq()`.
- New-repo column:
  - `new_repos`: CreateEvents with `ref_type='repository'`.
- PR columns:
  - `prs_opened`: PRs opened.
  - `prs_merged`: the brief's definition (closed with `merged=1`). It is blank from 2024-01.
  - `prs_merged_fixed`: closed with `merged_at` set.
  - `prs_merged_action`: `action='merged'`, only for 2025-12..2026-02.
- Merged-PR size columns, all using the `merged_at` definition:
  - `sum_additions` and `sum_deletions`.
  - `avg_additions`.
  - `median_additions`, from `quantileTDigest(0.5)`.
  - `avg_changed_files`.

**`payload_check.csv` (A2)** has the monthly shares used to locate breaks:

- `push_size_zero_share`, `push_distinct_size_zero_share` and `max_push_size`.
- `merged_prs_any_indicator`, which counts `merged=1`, `merged_at` set or `action='merged'`.
- `merged_flag_set_share` and `merged_zero_additions_and_deletions_share`.
- `opened_empty_body_share` and `opened_empty_title_share`.
- `create_repository_share`, `pr_events_new_action_share` (labeled, assigned or merged actions) and `prs_opened_per_push`.

It also has one status column per series: `status_commits`, `status_merged_flag`, `status_merged_pr_sizes`, `status_pr_body`, `status_new_repos` and `status_pr_counts`. Each takes one of: `ok`, `partial_break`, `broken`, `anomalous`, `decaying`, `partial_outage` or `no_data`.

**`agent_logins.csv` (A3 i)** lists the top 40 PR-opening logins for 2025-01..2026-06 that end in `[bot]` or match the AI name patterns, plus 47 more accounts from wider scans: AI-named bots and accounts that could be AI agents, each one classified.

- Columns: `login`, `category`, `product`, `top40_rank_2025_2026`, `prs_opened_2025_01_to_2026_06`, `prs_opened_2023_02_to_2026_06`, `repos_2023_02_to_2026_06`, `first_seen`, `last_seen`, `top_head_branch_prefixes` and `evidence`.
- `category` is one of:
  - `ai_coding_agent`: counted in the agent series.
  - `other_automation`.
  - `ai_related_excluded`: unverified, personal, or an internal instance.
- The 2025-01..2026-06 window effectively starts on 2025-09-25 because of the gap. `first_seen` is bounded by the coverage restarts on 2023-02-01 and 2025-09-25.
- The top 40 contains 6 AI agents: Copilot, google-labs-jules, devin-ai-integration, cto-new, codeflash-ai and netlify-coding.
- dependabot, renovate and github-actions are classed as other automation. So are vercel[bot] (41.7k CVE-patch PRs plus analytics-install PRs) and sourcery-ai (a rule-style refactoring bot).

**`agent_prs_monthly.csv` (A3 ii)** has monthly PRs opened by `ai_coding_agent` logins, grouped by product.

- Columns: `all_prs_opened`, `agent_prs_opened`, `agent_share_pct` and `agent_setup_prs_excluded`.
- Setup PRs (Configure Sweep, Snorkell setup, Junie init) are excluded from the agent counts.
- `ai_login_or_branch_prs` and `ai_login_or_branch_share_pct` count agent logins together with agent branch prefixes.
- There is one column per product, ordered by volume: `copilot_coding_agent`, `google_jules`, `devin`, `sweep`, `cto_new` and so on.
- `pr_count_status` flags 2025-10 and 2026-03 onward.
- `claude_agent_hq` and `codex_agent_hq` are the accounts named `Claude` and `Codex`. They have no `[bot]` suffix, like `Copilot`, and first appear on 2025-11-24.

**`signature_prs_monthly.csv` (A3 iii)** is in long format, playground only.

- Columns: `month`, `source`, `population` (`opened` or `merged`), `signal_type`, `signal`, `matched_prs`, `denominator_prs`, `share_pct`, `body_populated`, `coverage_status`, `pr_count_status` and `window_note`.
- `share_pct` is the share of all PRs in that population.
- `signal_type` is one of:
  - `body_signature`: only before 2025-10-08 17:00. 2025-10 covers Oct 1–8 only.
  - `head_branch_prefix`: all months.
  - `union`: an agent login or an agent branch, all months. Before the break it also counts body signatures.
- Body signals, all case-insensitive substrings:
  - `sig_generated_with_claude_code`: "Generated with [Claude Code]".
  - `sig_claude_ai_code_link`: claude.ai/code.
  - `sig_claude_code_mention`: "claude code".
  - `sig_coauthored_by_claude`: "co-authored-by: claude".
  - `sig_codex_link`: chatgpt.com/codex.
  - `sig_cursor_agent_link`: cursor.com/background-agent or cursor.com/agents.
  - `sig_devin_session_link`: devin.ai/sessions.
  - `sig_jules_link`: jules.google.
  - `sig_copilot_mention`: "copilot". This is broad and includes PR-summary tags and people mentioning Copilot.
  - `sig_any_specific`: the union of the specific signals, without Copilot.
  - `sig_any_incl_copilot`: the same union with Copilot.

**`signature_gap_samples.csv`** has the same columns, with `source=gharchive_sample`.

- It covers the gap months 2024-06..2025-09, using 2 hours a month. The sample counts are small, so only `share_pct` is meaningful.
- It adds `signal_type=agent_login`. Its agent counts include setup PRs, which matters only slightly, for Junie in Sep 2025.

**`sampled_hours.csv` (B)** has one row per raw hour.

- Columns: `hour_utc`, `year`, `weekday`, `is_weekend`, `role` (`baseline`, `extension` or `diagnostic`), `gz_mb`, `events_total`, `push_events`, `commits`, `distinct_commits`, `commits_cap1000`, `commits_lt1000`, `pushes_size_ge_1000`, `max_push_size`, `pushers`, `create_events`, `new_repos`, `prs_opened`, `prs_merged` (closed with `merged=true`), `prs_merged_action`, `merged_with_size`, `avg_additions`, `median_additions`, `avg_deletions`, `median_deletions`, `avg_changed_files` and `payload_note`.
- Values are blank where the payload no longer carries the field.

**`sampled_yearly.csv`** has one row per year, 2015–2025.

- For each metric it gives `n_hours_*`, `mean_per_hour_*` and `cv_*` (the coefficient of variation across the sample hours).
- `est_annual_*` is the specified **estimate**: mean per hour × hours in the year.
- `est_annual_adj_*` is the day-type-adjusted **estimate**, defined under Methods.
- `pushers` is distinct pushers per hour and is not annualised.
- The pooled size columns are `merged_prs_with_size`, `pooled_median_additions`, `mean_of_hourly_median_additions`, `pooled_median_deletions` and `pooled_avg_additions`.

**`validation.csv`** compares the sample estimates with the playground truth (table below).

- Columns: `check`, `window`, `metric`, `sample_hours`, `n_samples`, `weekend_samples`, `sample_mean_per_hour`, `cv_across_samples`, `multiplier_hours`, `estimate_raw`, `estimate_adj`, `truth`, `pct_error_raw`, `pct_error_adj`, `factor_window` and `note`.

**`hour15_factors.csv`** has the day-type factors: the mean at 15:00 UTC on weekdays and on weekend days, divided by the mean over all hours. They are given per metric and per calibration window. Low-volume and anomaly hours are excluded.

**`source_agreement.csv`** compares the same hour in a raw file and in the playground. All 9 overlapping hours match exactly, except `pushers`, which differs by 1 in one hour because the playground uses the approximate `uniq()`. Both sources therefore measure the same thing.

**`queries.sql`** has 60 statements, exactly as run, each with a one-line comment recording the outcome.

- 3 failed because of a shell quoting slip and are kept as run. The "rows" figure in each comment is the number of output lines.
- The final statements are labelled:
  - "A1 (final, re-run)" feeds `monthly.csv`.
  - "A2 (final)" feeds `payload_check.csv`.
  - "A3(ii) (final)" and "A3 extra: monthly union" feed `agent_prs_monthly.csv`.
  - "A3(iii)" for opened and for merged PRs, "A3 extra: monthly opened PRs whose head branch" and "A3 extra: monthly union" feed `signature_prs_monthly.csv`.
  - "Hourly table v2" and "Validation truth" feed `validation.csv`.

**`scripts/`** holds the scripts:

- `ch.py`: the query runner and logger.
- `sample_gharchive.py`: Source B.
- `sample_signatures.py`: the gap samples.
- `hour15_drift_check.py`, `inspect_schema.py` and `build_outputs.py`.

**`work/`** holds raw query outputs and sample records (jsonl).

## Validation (sample estimator against playground truth, same 15:00 UTC hours)

Notes on the windows:

- **2023**: Feb–Dec. The multiplier is the 7,975 file hours present, out of 8,016.
- **2024 H1**: only the Feb and May samples exist, because Aug and Nov fall in the gap. The truth runs from Jan 1 to Jun 5 08:59. Commit metrics exclude the 2024-04-16..05-06 anomaly hours.
- **2025–26**: there is no true 2025 total, so this substitutes Nov 2025–May 2026 with 3 samples. Only the fields that survive the break can be checked.
- The adjusted estimates use factors from outside the test window.

| Window | Metric | Samples | CV across hours | Raw estimate | Adjusted estimate | Truth | Raw error | Adjusted error |
|---|---|---|---|---|---|---|---|---|
| 2023 | push_events | 4 (0 weekend) | 0.14 | 835.3M | 753.9M | 760.6M | +9.8% | −0.9% |
| 2023 | commits | 4 (0) | 0.33 | 3,573M | 2,649M | 2,895M | +23.4% | −8.5% |
| 2023 | commits_cap1000 | 4 (0) | 0.12 | 2,667M | 2,049M | 2,190M | +21.8% | −6.5% |
| 2023 | commits_lt1000 | 4 (0) | 0.12 | 2,103M | 1,668M | 1,719M | +22.3% | −3.0% |
| 2023 | new_repos | 4 (0) | 0.13 | 66.7M | 50.6M | 53.2M | +25.2% | −5.0% |
| 2023 | prs_opened | 4 (0) | 0.16 | 63.2M | 45.8M | 49.1M | +28.7% | −6.8% |
| 2023 | prs_merged | 4 (0) | 0.16 | 48.9M | 33.2M | 33.8M | +44.6% | −1.8% |
| 2023 | pushers per hour | 4 (0) | 0.12 | 41,179 | 28,727 | 28,938 | +42.3% | −0.7% |
| 2023 | median additions | 4 (0) | 0.06 | 22.0 | – | 22 | 0.0% | – |
| 2024 H1 | push_events | 2 (0) | 0.01 | 536.8M | 485.4M | 511.6M | +4.9% | −5.1% |
| 2024 H1 | commits_cap1000 | 2 (0) | 0.02 | 1,315M | 1,078M | 1,008M | +30.4% | +6.9% |
| 2024 H1 | commits_lt1000 | 2 (0) | 0.04 | 1,045M | 870M | 842M | +24.1% | +3.3% |
| 2024 H1 | new_repos | 2 (0) | 0.01 | 36.5M | 29.8M | 26.5M | +37.7% | +12.2% |
| 2024 H1 | prs_opened | 2 (0) | 0.07 | 34.7M | 27.6M | 24.0M | +44.2% | +14.6% |
| 2024 H1 | prs_merged | 2 (0) | 0.02 | 26.6M | 19.5M | 17.3M | +53.7% | +12.7% |
| 2024 H1 | pushers per hour | 2 (0) | 0.03 | 46,038 | 33,481 | 31,750 | +45.0% | +5.5% |
| 2024 H1 | median additions | 2 (0) | 0.09 | 22.5 | – | 21 | +7.1% | – |
| 2025–26 | push_events | 3 (2) | 0.03 | 526.7M | 507.5M | 543.9M | −3.2% | −6.7% |
| 2025–26 | prs_opened | 3 (2) | 0.76 | 16.3M | 21.1M | 18.0M | −9.5% | +17.5% |
| 2025–26 | pushers per hour | 3 (2) | 0.14 | 39,915 | 34,844 | 40,007 | −0.2% | −12.9% |

How to read it:

- With weekday-only samples, the raw estimator overshoots by 5–54%. 15:00 UTC on a weekday is 1.11× the average hour for pushes and 1.29–1.40× for PRs, while weekend 15:00 is 0.76–1.15×.
- In the 2025–26 window the raw estimator lands within 10%, but only by luck: two weekend samples offset the weekday bias.
- The adjusted estimator is the better choice for trends.
- Sampling noise alone is about ±6–8% for a mean of 4 hours (CV 0.12–0.16).

## Methods

- **Source B estimate**: `est_annual = mean(4 hours) × hours in the year` (8,760, or 8,784 in leap years).
- **Adjusted estimate**: `est_annual_adj = hours × mean(x_i / f(daytype_i))`.
  - f is the 15:00 UTC factor for weekdays or weekend days, taken from `hour15_factors.csv` for the pre-gap window 2023-01-13..2024-06-05.
  - Weekday factors: push_events 1.107, commits_cap1000 1.245, new_repos 1.254, prs_opened 1.293, prs_merged 1.396 and pushers 1.392.
  - Weekend factors: 1.008, 0.942, 1.145, 0.756, 0.838 and 1.032, in the same order.
- **Drift check**: the ratio of the 15:00 hour to the daily mean was measured on one mid-May Wednesday per year, using full raw days.

| Metric | 2015 | 2019 | 2023–24 Wednesdays (median of 69) |
|---|---|---|---|
| Pushes | 1.44 | 1.31 | 1.07 |
| PRs opened | 1.56 | 1.28 | 1.15 |
| PRs merged | 1.56 | 1.38 | 1.27 |
| New repos | 1.29 | 1.22 | 1.20 |

  So applying 2023–24 factors overstates 2015 by roughly 7–36% and 2019 by 2–22%, depending on the metric. These are single days, so each ratio carries about ±10% noise.
- **Agent branch prefixes** were checked against body signatures and logins in the last window with full payloads (2025-09-25..10-08):

| Prefix | Precision | Recall |
|---|---|---|
| `codex/` | 99.4% | 94.8% |
| `copilot/` | 98.2% | 100% |
| `cursor/` | 90.7% | 99.8% |
| `devin/` | 94.9% | 84.0% |
| `claude/` | 88.6% | 4.0% |

  Recall for `claude/` was low then because Claude Code CLI PRs used users' own branch names; `claude/` branches took off with Claude Code on the web. Treat `claude/` counts as a lower bound.
- **Gap-sample hours**: across the hours of the day, the AI-signature share ranged from 6.8% to 9.1%. The 03:00+15:00 average was 8.2%, against 8.0% for all hours.
- **Python matching check**: the Python raw-file matcher reproduces the playground counts exactly for 2025-10-01 15:00.

## Unverified or limited

- **Agent identity from names only**: some accounts appear only after the payload break, so they have no titles or bodies to check. They are cto-new, Claude, Codex, kiro-agent, tembo, kilo-code and capy-ai. `Claude` and `Codex` look like GitHub Agent HQ agents, but this is unverified.
- **AI shares are lower bounds.** IDE assistants, and Claude Code CLI use on user-named branches, leave no trace in public events.
- **2025 annual values** rest on 3–4 sample hours, 2 of them weekends. In GH Archive, 2025-08-15 is a low-volume hour. The adjusted 2024→2025 change (−6% to +3%) is within noise.
- **Post-break PR levels are lower than before the gap**: about 3.2M opened a month against about 4.8M in early 2024, while pushers rose. Whether that is real or a coverage change is unverified. The raw files match the playground, so the change is upstream of the playground.
- **Jules dropped 95% in Feb 2026** (45k to 2.3k PRs a month). This is probably a change in which account authors its PRs, but that is unverified.
- **Drift correction**: no correction for the 2015–2022 drift was applied. Only its direction and rough size are given.
