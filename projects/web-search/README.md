# web-search

**Web search and page fetch CLI tool for AI agents.**

Part of the agent-native toolkit. Uses Brave Search API for web search with generous free tier (2000 queries/month).

## Features

- **search** — Web search with Brave Search API
- **fetch** — Extract readable content from any URL
- **summarize** — Extractive summarization of URL content
- **doctor** — Check API configuration

## Setup

```bash
# Set your Brave Search API key
export BRAVE_SEARCH_KEY="your_key_here"

# Get a free key at: https://brave.com/search/api/
```

## Usage

```bash
# Search the web
python cli.py search "OpenClaw AI agent"
python cli.py search "linux-server-skill" --count 10 --freshness week

# Fetch page content
python cli.py fetch "https://github.com/michael-ltm/linux-server-skill"

# Summarize a URL
python cli.py summarize "https://example.com/article"

# Check API status
python cli.py doctor
```

## Requirements

- Python 3.8+
- `requests` library

```bash
pip install requests
```

## Verification

```bash
cd projects/web-search
export BRAVE_SEARCH_KEY="your_key"
python cli.py doctor    # Should show ✅ API is working
python cli.py search "test"
```

## Skill Trigger

This tool is activated when the user mentions:
- "search the web", "look up", "find online"
- "fetch this URL", "read this page", "scrape"
- "summarize this", "what's on this page"
