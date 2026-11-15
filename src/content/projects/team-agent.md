---
title: An agent for the team
summary: An autonomous engineering agent connected through MCP to our workspace, Datadog and codebase. It reviews code, raises PRs, reviews docs and keeps track of project status.
org: Rokt
period: 2026
stack: [Claude, MCP, Datadog]
order: 5
---

## What it does

- Reviews code on its own.
- Raises pull requests.
- Reviews design docs.
- Keeps context and status across several workstreams.

## How

It connects through MCP (Model Context Protocol) servers to the workspace suite, Datadog and the codebase.
