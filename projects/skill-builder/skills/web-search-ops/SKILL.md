---
name: web-search-ops
description: Search the web for real-time information using Brave Search API. Fetch and extract content from URLs. Use when: researching topics, finding current information, verifying facts, or looking up documentation.
---

# Web Search Ops

## When to Use

Use this skill when the user mentions: search, find, look up, web, internet, browse, fetch.


## SENSITIVE DATA

Search queries are sent to Brave Search API. No authentication credentials stored. User IP visible to Brave.

## Session Start

Confirm Brave Search API key is configured in environment (BRAVE_SEARCH_KEY). If missing, inform user.

## Commands

- `search <query>` — web search with Brave API
- `fetch <url>` — extract readable content from URL
- `summarize <url>` — summarize URL content

## Quality Standards

- Always verify destructive operations before executing
- Report progress clearly during long-running tasks
- Mask all sensitive data in output
- Maintain context between commands in a session
