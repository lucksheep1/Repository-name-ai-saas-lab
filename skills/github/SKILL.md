---
name: github-cli
description: Interact with GitHub using the gh CLI. Use this skill for gh issue, gh pr, gh run, and gh api flows. This skill is distinct from github-api, which uses the Maton gateway.
metadata:
  clawdbot:
    emoji: "🐙"
    requires:
      bins:
        - gh
---

# GitHub CLI

Use this skill when the task should run through the local gh command line tool.
Do not confuse it with github-api, which calls the Maton gateway over HTTP.

## Required Dependency

- gh

## Current Status

- gh: missing on the current server
- Fallback: limited. Use github-api only if API-style access is acceptable and MATON_API_KEY is configured.

## Pull Requests

Check CI status on a PR:
```bash
gh pr checks 55 --repo owner/repo
```

List recent workflow runs:
```bash
gh run list --repo owner/repo --limit 10
```

View a run and see which steps failed:
```bash
gh run view <run-id> --repo owner/repo
```

View logs for failed steps only:
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

## API for Advanced Queries

The gh api command is useful for accessing data not available through other subcommands.

```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON Output

Most commands support --json for structured output. You can use --jq to filter:

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```
