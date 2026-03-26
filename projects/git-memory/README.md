# git-memory

**Ask questions about your git history in natural language.**

Uses agent-memory to store git context, enabling smarter Q&A about your repository's history, patterns, and changes.

## Features

- **Ask questions** about your git history in plain English
- **Track context** — store important decisions, patterns, and notes alongside your git history
- **Analyze patterns** — commit frequency, top contributors, file change patterns
- **Time-based queries** — "what changed last Tuesday?", "who worked on this last week?"

## Usage

```bash
# Ask a question about your git history
python git_memory.py --storage json --path ./git_memory.json ask "what did we change last Tuesday?"

# Show recent commits
python git_memory.py --storage json --path ./git_memory.json log --limit 20

# Show git statistics
python git_memory.py --storage json --path ./git_memory.json stats

# Add important context to memory
python git_memory.py --storage json --path ./git_memory.json add-context "deprecated the old API in v2.3" --category deprecation

# Show diff for a commit
python git_memory.py --storage json --path ./git_memory.json diff --commit abc1234
```

## Questions you can ask

- "what changed last week?"
- "who made the most commits?"
- "what files changed most frequently?"
- "show me all bug fixes from the last month?"
- "what was committed on last Tuesday?"

## Setup

Requires `agent-memory` as a sibling directory or in your Python path:

```bash
cd projects/git-memory
cd .. && git clone https://github.com/lucksheep1/Repository-name-ai-saas-lab.git
# or: pip install agent-memory
```

## How it works

- Parses `git log` output into structured data
- Stores git context in agent-memory for conversational recall
- Answers natural language queries by pattern-matching against git history
- Time-aware: understands "last Tuesday", "2 weeks ago", etc.

## Example

```bash
$ python git_memory.py ask "what did we change last week?"
🔍 Question: what did we change last week?

📅 Found 47 commits from the last 7 days:

  [f3cce7a] 2026-03-26 AI SaaS Lab
      fix: send site-tracker report via message tool

  [ab29d31] 2026-03-26 AI SaaS Lab
      feat: add dashboard.py - standalone HTML analytics

  ...
```

## Verification

```bash
cd projects/git-memory
python git_memory.py --storage json --path /tmp/test.json stats
# Should show: Total commits, branches, recent activity
```

## Limits

- Requires `git` CLI installed
- Time queries use natural language parsing (simple keyword matching)
- Does not connect to GitHub/GitLab APIs (local git only)
- Memory storage: uses agent-memory (json/sqlite/redis)

## Next steps

- Add GitHub API integration for remote repo queries
- Add branch comparison queries
- Add semantic search over commit messages
