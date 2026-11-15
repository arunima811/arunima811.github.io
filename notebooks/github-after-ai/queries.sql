-- Final queries behind the post, run on https://play.clickhouse.com (table github_events).

-- A3(iii): monthly opened PRs whose body carries AI-tool signatures (case-insensitive), only before the 2025-10-08 17:00 UTC payload break when body is populated [ok, 19 rows, 8s]
SELECT
    toStartOfMonth(created_at) AS month,
    count() AS prs_opened,
    countIf(body != '') AS prs_opened_with_body,
    countIf(positionCaseInsensitive(body, 'Generated with [Claude Code]') > 0) AS sig_generated_with_claude_code,
    countIf(positionCaseInsensitive(body, 'claude.ai/code') > 0) AS sig_claude_ai_code_link,
    countIf(positionCaseInsensitive(body, 'claude code') > 0) AS sig_claude_code_mention,
    countIf(positionCaseInsensitive(body, 'co-authored-by: claude') > 0) AS sig_coauthored_by_claude,
    countIf(positionCaseInsensitive(body, 'chatgpt.com/codex') > 0) AS sig_codex_link,
    countIf(multiSearchAnyCaseInsensitive(body, ['cursor.com/background-agent', 'cursor.com/agents']) > 0) AS sig_cursor_agent_link,
    countIf(positionCaseInsensitive(body, 'devin.ai/sessions') > 0) AS sig_devin_session_link,
    countIf(positionCaseInsensitive(body, 'jules.google') > 0) AS sig_jules_link,
    countIf(positionCaseInsensitive(body, 'copilot') > 0) AS sig_copilot_mention,
    countIf(multiSearchAnyCaseInsensitive(body, ['claude code', 'claude.ai/code', 'co-authored-by: claude', 'chatgpt.com/codex', 'cursor.com/background-agent', 'cursor.com/agents', 'devin.ai/sessions', 'jules.google']) > 0) AS sig_any_specific,
    countIf(multiSearchAnyCaseInsensitive(body, ['claude code', 'claude.ai/code', 'co-authored-by: claude', 'chatgpt.com/codex', 'cursor.com/background-agent', 'cursor.com/agents', 'devin.ai/sessions', 'jules.google', 'copilot']) > 0) AS sig_any_incl_copilot
FROM github_events
WHERE event_type = 'PullRequestEvent' AND action = 'opened'
  AND created_at >= '2023-02-01 00:00:00' AND created_at < '2025-10-08 17:00:00'
GROUP BY month
ORDER BY month FORMAT CSVWithNames;

-- A3(iii): same AI-tool body signatures for merged PRs (closed with merged_at set; the merged flag is broken after 2024-01-07 19:00), before the 2025-10-08 17:00 break [ok, 19 rows, 4s]
SELECT
    toStartOfMonth(created_at) AS month,
    count() AS prs_merged,
    countIf(body != '') AS prs_merged_with_body,
    countIf(positionCaseInsensitive(body, 'Generated with [Claude Code]') > 0) AS sig_generated_with_claude_code,
    countIf(positionCaseInsensitive(body, 'claude.ai/code') > 0) AS sig_claude_ai_code_link,
    countIf(positionCaseInsensitive(body, 'claude code') > 0) AS sig_claude_code_mention,
    countIf(positionCaseInsensitive(body, 'co-authored-by: claude') > 0) AS sig_coauthored_by_claude,
    countIf(positionCaseInsensitive(body, 'chatgpt.com/codex') > 0) AS sig_codex_link,
    countIf(multiSearchAnyCaseInsensitive(body, ['cursor.com/background-agent', 'cursor.com/agents']) > 0) AS sig_cursor_agent_link,
    countIf(positionCaseInsensitive(body, 'devin.ai/sessions') > 0) AS sig_devin_session_link,
    countIf(positionCaseInsensitive(body, 'jules.google') > 0) AS sig_jules_link,
    countIf(positionCaseInsensitive(body, 'copilot') > 0) AS sig_copilot_mention,
    countIf(multiSearchAnyCaseInsensitive(body, ['claude code', 'claude.ai/code', 'co-authored-by: claude', 'chatgpt.com/codex', 'cursor.com/background-agent', 'cursor.com/agents', 'devin.ai/sessions', 'jules.google']) > 0) AS sig_any_specific,
    countIf(multiSearchAnyCaseInsensitive(body, ['claude code', 'claude.ai/code', 'co-authored-by: claude', 'chatgpt.com/codex', 'cursor.com/background-agent', 'cursor.com/agents', 'devin.ai/sessions', 'jules.google', 'copilot']) > 0) AS sig_any_incl_copilot
FROM github_events
WHERE event_type = 'PullRequestEvent' AND action = 'closed' AND merged_at > toDateTime('1970-01-01 00:00:00')
  AND created_at >= '2023-02-01 00:00:00' AND created_at < '2025-10-08 17:00:00'
GROUP BY month
ORDER BY month FORMAT CSVWithNames;

-- A3 extra: monthly opened PRs whose head branch starts with an agent prefix (claude/, codex/, copilot/, cursor/, devin/); works across the Oct-2025 payload break [ok, 27 rows, 0s]
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

-- A2 (final): monthly payload-break shares - PushEvents with push_size=0, merged PRs with additions=0 and deletions=0, opened PRs with empty body (plus title, CreateEvent repository share, new PR actions, PRs per push) [ok, 27 rows, 6s]
SELECT
    toStartOfMonth(created_at) AS month,
    countIf(event_type = 'PushEvent') AS push_events,
    round(countIf(event_type = 'PushEvent' AND push_size = 0) / countIf(event_type = 'PushEvent'), 5) AS push_size_zero_share,
    round(countIf(event_type = 'PushEvent' AND push_distinct_size = 0) / countIf(event_type = 'PushEvent'), 5) AS push_distinct_size_zero_share,
    maxIf(push_size, event_type = 'PushEvent') AS max_push_size,
    countIf(event_type = 'PullRequestEvent' AND ((action = 'closed' AND (merged = 1 OR merged_at > toDateTime('1970-01-01 00:00:00'))) OR action = 'merged')) AS merged_prs_any_indicator,
    round(countIf(event_type = 'PullRequestEvent' AND action = 'closed' AND merged = 1) / countIf(event_type = 'PullRequestEvent' AND action = 'closed' AND merged_at > toDateTime('1970-01-01 00:00:00')), 5) AS merged_flag_set_share,
    round(countIf(event_type = 'PullRequestEvent' AND ((action = 'closed' AND (merged = 1 OR merged_at > toDateTime('1970-01-01 00:00:00'))) OR action = 'merged') AND additions = 0 AND deletions = 0)
          / countIf(event_type = 'PullRequestEvent' AND ((action = 'closed' AND (merged = 1 OR merged_at > toDateTime('1970-01-01 00:00:00'))) OR action = 'merged')), 5) AS merged_zero_additions_and_deletions_share,
    countIf(event_type = 'PullRequestEvent' AND action = 'opened') AS opened_prs,
    round(countIf(event_type = 'PullRequestEvent' AND action = 'opened' AND body = '') / countIf(event_type = 'PullRequestEvent' AND action = 'opened'), 5) AS opened_empty_body_share,
    round(countIf(event_type = 'PullRequestEvent' AND action = 'opened' AND title = '') / countIf(event_type = 'PullRequestEvent' AND action = 'opened'), 5) AS opened_empty_title_share,
    countIf(event_type = 'CreateEvent') AS create_events,
    round(countIf(event_type = 'CreateEvent' AND ref_type = 'repository') / countIf(event_type = 'CreateEvent'), 5) AS create_repository_share,
    round(countIf(event_type = 'PullRequestEvent' AND action IN ('labeled', 'unlabeled', 'assigned', 'unassigned', 'merged')) / countIf(event_type = 'PullRequestEvent'), 5) AS pr_events_new_action_share,
    round(countIf(event_type = 'PullRequestEvent' AND action = 'opened') / countIf(event_type = 'PushEvent'), 5) AS prs_opened_per_push
FROM github_events
WHERE event_type IN ('PushEvent', 'PullRequestEvent', 'CreateEvent')
  AND created_at >= '2023-02-01 00:00:00' AND created_at < '2026-07-01 00:00:00'
GROUP BY month
ORDER BY month FORMAT CSVWithNames;

-- A3(ii) (final): monthly PRs opened by AI-agent logins grouped by product, split by onboarding/setup PRs (Configure Sweep, Snorkell setup, Junie init), plus all PRs opened (agent=empty), 2023-02..2026-06 [ok, 383 rows, 1s]
SELECT
    toStartOfMonth(created_at) AS month,
    multiIf(
        actor_login = 'Copilot', 'copilot_coding_agent',
        actor_login = 'google-labs-jules[bot]', 'google_jules',
        actor_login IN ('devin-ai-integration[bot]', 'staging-devin-ai-integration[bot]'), 'devin',
        actor_login = 'cto-new[bot]', 'cto_new',
        actor_login IN ('sweep-ai[bot]', 'sweep-nightly[bot]', 'sweep-canary[bot]'), 'sweep',
        actor_login = 'claude[bot]', 'claude_code_github_app',
        actor_login = 'Claude', 'claude_agent_hq',
        actor_login = 'Codex', 'codex_agent_hq',
        actor_login = 'cursor[bot]', 'cursor_agent',
        actor_login = 'netlify-coding[bot]', 'netlify_agent_runners',
        actor_login = 'codeflash-ai[bot]', 'codeflash',
        actor_login = 'coderabbitai[bot]', 'coderabbit',
        actor_login = 'e2b-for-github[bot]', 'e2b',
        actor_login = 'snorkell-ai[bot]', 'snorkell',
        actor_login = 'genspark-ai-developer[bot]', 'genspark',
        actor_login IN ('blitzy[bot]', 'blitzy-qa[bot]'), 'blitzy',
        actor_login = 'jetbrains-junie[bot]', 'jetbrains_junie',
        actor_login = 'opencode-agent[bot]', 'opencode',
        actor_login = 'codegen-sh[bot]', 'codegen',
        actor_login = 'kiro-agent[bot]', 'kiro',
        actor_login IN ('roomote[bot]', 'roomote-v0[bot]'), 'roo_code_roomote',
        actor_login = 'tembo[bot]', 'tembo',
        actor_login IN ('kilo-code-bot[bot]', 'kiloconnect[bot]'), 'kilo_code',
        actor_login = 'amazon-q-developer[bot]', 'amazon_q_developer',
        actor_login = 'factory-droid[bot]', 'factory_droid',
        actor_login = 'capy-ai[bot]', 'capy',
        actor_login = 'gitauto-ai[bot]', 'gitauto',
        actor_login = 'ellipsis-dev[bot]', 'ellipsis',
        actor_login = 'cubic-dev-ai[bot]', 'cubic',
        actor_login IN ('seer-by-sentry[bot]', 'sentry-ai-autofix-experimental[bot]'), 'sentry_seer',
        actor_login IN ('komment-ai[bot]', 'komment-ai-dev[bot]', 'komment-ai-beta[bot]'), 'komment',
        actor_login = 'codeant-ai[bot]', 'codeant',
        '') AS agent,
    (title IN ('Configure Sweep', 'Sweep: Configure Sweep')
     OR startsWith(title, '[Snorkell.ai]: Setting up')
     OR startsWith(title, 'Initialize JetBrains Junie')
     OR startsWith(lower(head_ref), 'junie-init')
     OR startsWith(head_ref, 'sweep/add-sweep-config')
     OR startsWith(head_ref, 'snorkell_ai/config')
     OR startsWith(head_ref, 'snorkell_ai/setup')) AS is_setup_pr,
    count() AS prs_opened
FROM github_events
WHERE event_type = 'PullRequestEvent' AND action = 'opened'
  AND created_at >= '2023-02-01 00:00:00' AND created_at < '2026-07-01 00:00:00'
GROUP BY month, agent, is_setup_pr
ORDER BY month, agent, is_setup_pr FORMAT CSVWithNames;

-- A1 (final, re-run): identical to the previous A1 final statement; re-run because its local output was overwritten while tidying files [ok, 27 rows, 2s]
SELECT
    toStartOfMonth(created_at) AS month,
    countIf(event_type = 'PushEvent') AS push_events,
    sumIf(push_size, event_type = 'PushEvent') AS commits,
    sumIf(push_distinct_size, event_type = 'PushEvent') AS distinct_commits,
    sumIf(least(push_size, 1000), event_type = 'PushEvent') AS commits_cap1000,
    sumIf(push_size, event_type = 'PushEvent' AND push_size < 1000) AS commits_lt1000,
    countIf(event_type = 'PushEvent' AND push_size >= 1000) AS pushes_ge_1000,
    uniqIf(actor_login, event_type = 'PushEvent') AS pushers,
    countIf(event_type = 'CreateEvent' AND ref_type = 'repository') AS new_repos,
    countIf(event_type = 'PullRequestEvent' AND action = 'opened') AS prs_opened,
    countIf(event_type = 'PullRequestEvent' AND action = 'closed' AND merged = 1) AS prs_merged,
    countIf(event_type = 'PullRequestEvent' AND action = 'closed' AND merged_at > toDateTime('1970-01-01 00:00:00')) AS prs_merged_fixed,
    countIf(event_type = 'PullRequestEvent' AND action = 'merged') AS prs_merged_action,
    sumIf(additions, event_type = 'PullRequestEvent' AND action = 'closed' AND merged_at > toDateTime('1970-01-01 00:00:00')) AS sum_additions,
    sumIf(deletions, event_type = 'PullRequestEvent' AND action = 'closed' AND merged_at > toDateTime('1970-01-01 00:00:00')) AS sum_deletions,
    round(avgIf(additions, event_type = 'PullRequestEvent' AND action = 'closed' AND merged_at > toDateTime('1970-01-01 00:00:00')), 2) AS avg_additions,
    round(quantileTDigestIf(0.5)(additions, event_type = 'PullRequestEvent' AND action = 'closed' AND merged_at > toDateTime('1970-01-01 00:00:00')), 2) AS median_additions,
    round(avgIf(changed_files, event_type = 'PullRequestEvent' AND action = 'closed' AND merged_at > toDateTime('1970-01-01 00:00:00')), 3) AS avg_changed_files,
    uniq(toStartOfHour(created_at)) AS hours_with_data,
    toUInt32(dateDiff('hour', toStartOfMonth(created_at), addMonths(toStartOfMonth(created_at), 1))) AS hours_in_month
FROM github_events
WHERE event_type IN ('PushEvent', 'CreateEvent', 'PullRequestEvent')
  AND created_at >= '2023-02-01 00:00:00' AND created_at < '2026-07-01 00:00:00'
GROUP BY month
ORDER BY month FORMAT CSVWithNames;

-- A3 extra: monthly union of AI signals on opened PRs - AI-agent login (setup PRs excluded) OR agent branch prefix (all months), plus body signature (before the 2025-10-08 17:00 break) [ok, 27 rows, 4s]
SELECT
    toStartOfMonth(created_at) AS month,
    count() AS prs_opened,
    countIf(is_agent_login) AS by_ai_agent_login,
    countIf(has_agent_branch) AS with_agent_branch_prefix,
    countIf(is_agent_login OR has_agent_branch) AS ai_login_or_branch,
    countIf(created_at < '2025-10-08 17:00:00') AS prs_opened_before_payload_break,
    countIf(created_at < '2025-10-08 17:00:00' AND (is_agent_login OR has_agent_branch OR has_body_signature)) AS ai_login_branch_or_body_before_break
FROM
(
    SELECT
        created_at,
        actor_login IN ('Copilot', 'google-labs-jules[bot]', 'devin-ai-integration[bot]', 'staging-devin-ai-integration[bot]', 'cto-new[bot]',
                        'sweep-ai[bot]', 'sweep-nightly[bot]', 'sweep-canary[bot]', 'claude[bot]', 'Claude', 'Codex', 'cursor[bot]',
                        'netlify-coding[bot]', 'codeflash-ai[bot]', 'coderabbitai[bot]', 'e2b-for-github[bot]', 'snorkell-ai[bot]',
                        'genspark-ai-developer[bot]', 'blitzy[bot]', 'blitzy-qa[bot]', 'jetbrains-junie[bot]', 'opencode-agent[bot]',
                        'codegen-sh[bot]', 'kiro-agent[bot]', 'roomote[bot]', 'roomote-v0[bot]', 'tembo[bot]', 'kilo-code-bot[bot]',
                        'kiloconnect[bot]', 'amazon-q-developer[bot]', 'factory-droid[bot]', 'capy-ai[bot]', 'gitauto-ai[bot]',
                        'ellipsis-dev[bot]', 'cubic-dev-ai[bot]', 'seer-by-sentry[bot]', 'sentry-ai-autofix-experimental[bot]',
                        'komment-ai[bot]', 'komment-ai-dev[bot]', 'komment-ai-beta[bot]', 'codeant-ai[bot]')
          AND NOT (title IN ('Configure Sweep', 'Sweep: Configure Sweep') OR startsWith(title, '[Snorkell.ai]: Setting up')
                   OR startsWith(title, 'Initialize JetBrains Junie') OR startsWith(lower(head_ref), 'junie-init')
                   OR startsWith(head_ref, 'sweep/add-sweep-config') OR startsWith(head_ref, 'snorkell_ai/config')
                   OR startsWith(head_ref, 'snorkell_ai/setup')) AS is_agent_login,
        match(lower(head_ref), '^(claude|codex|copilot|cursor|devin)/') AS has_agent_branch,
        multiSearchAnyCaseInsensitive(body, ['claude code', 'claude.ai/code', 'co-authored-by: claude', 'chatgpt.com/codex',
                                             'cursor.com/background-agent', 'cursor.com/agents', 'devin.ai/sessions', 'jules.google']) > 0 AS has_body_signature
    FROM github_events
    WHERE event_type = 'PullRequestEvent' AND action = 'opened'
      AND created_at >= '2023-02-01 00:00:00' AND created_at < '2026-07-01 00:00:00'
)
GROUP BY month
ORDER BY month FORMAT CSVWithNames;
