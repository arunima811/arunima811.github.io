# GitHub Search API counts (January 2022 to October 2026)

Pulled 15–16 November 2026 UTC, read-only (GET only), with a personal token. Each number is the `total_count` of one GitHub search. Months are UTC calendar months.

## Files

| File | Contents |
|---|---|
| `monthly.csv` | One row per month, 2022-01..2026-10. Counts: `merged_prs`, `opened_prs`, `new_repos`, and the AI-tool signals `copilot_agent`, `jules`, `devin`, `codex`, `claude_code`, `cursor_agents`, `cursor_background_agent`, `branch_codex`, `branch_copilot`, `branch_claude`, `branch_cursor`, `branch_devin`. Each has a `<metric>_flag`: `ok` (complete on the first try) or `missing` (not run). |
| `validation_vs_gharchive.csv` | GH Archive monthly counts (`../monthly.csv`) against Search, with the GH Archive ÷ Search ratios. |
| `branch_prefix_check.csv` | The test of the `head:` qualifier, one row per branch prefix. |
| `../../scripts/ghpull.py` | Reruns everything: `python3 ghpull.py monthly base`, then `monthly branch`, then `validate`. Set `GH_TOKEN` to your own token. It writes progress files next to itself and logs every call to `queries.log`. |

## Queries

All queries use `search/issues` (or `search/repositories` for new repos), with `per_page=1`, and read `total_count`. `{r}` is `{YYYY-MM-01}..{last day of the month}`.

| Metric | Query |
|---|---|
| Merged PRs | `is:pr is:merged merged:{r}` |
| Opened PRs | `is:pr created:{r}` |
| New repos | `created:{r}` on `search/repositories` (forks are excluded by default) |
| Copilot coding agent | `is:pr created:{r} author:app/copilot-swe-agent` |
| Jules | `is:pr created:{r} author:app/google-labs-jules` |
| Devin | `is:pr created:{r} author:app/devin-ai-integration` |
| Codex link | `is:pr created:{r} "chatgpt.com/codex" in:body` |
| Claude Code footer | `is:pr created:{r} "Generated with Claude Code" in:body` |
| Cursor | `is:pr created:{r} "cursor.com/agents" in:body` and `"cursor.com/background-agent" in:body` |
| Branch prefixes | `is:pr created:{r} head:<prefix>/` for `codex`, `copilot`, `claude`, `cursor`, `devin` |

- **Completeness.** All 761 count queries returned `incomplete_results=false` on the first try. Branch counts cover 2024-01..2026-10, plus 2022-01..02 as a baseline; the other 2022–2023 branch cells were not run.
- **Pacing.** Search calls were at least 2.3 s apart (6 s for `head:` queries). Eight secondary-rate-limit responses were retried after a backoff and succeeded.
- **Branch prefixes.** `head:<prefix>/` is a prefix match: in October 2025 it found 3 of 3 known PRs per tool, and 20 of 20 top results per prefix had a branch starting with the prefix. Branch names are chosen by people too, so tying a prefix to one tool is approximate.
- **Body markers.** 30 of 30 sampled bodies contained the Claude Code footer (October 2026) and the Codex link (October 2025). Codex stopped adding its link during November 2025, so the post uses the larger of the link and `codex/` counts. 25 of 30 `cursor.com/agents` bodies also had `cursor.com/background-agent`, so the post takes the larger of the two and never adds them.

## Caveats

- **Search shows today's state.** Deleted PRs, spam GitHub has removed and private repositories are left out. Recent months have had less time for spam cleanup, so late 2026 may be overstated by an unknown amount. A rerun on 18 November 2026 counted October 2026 merged PRs at 26,270,556, 0.2% below the 26,325,337 counted two to three days earlier.
- **Opened PRs are noisy.** Spam and bot waves cause spikes (February and December 2022), so the post's volume charts use merged PRs.
- **Signals overlap and miss things.** Tool signals are added without removing overlap, and they miss AI help that leaves no trace (editor assistants, deleted footers).
- **GH Archive comparison.** For 2023-02..2024-05 the GH Archive ÷ Search ratio for merged PRs had a median of 0.978 (range 0.938–1.027). For 2025-11..2026-02 it was 0.29–0.39 (opened PRs; merged PRs 0.30–0.38). The cause is not verified.
