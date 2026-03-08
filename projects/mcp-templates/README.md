# MCP Server Templates

Quick-start templates for Model Context Protocol (MCP) servers.

## Problem

Creating an MCP server from scratch is tedious:
- No simple templates
- Complex boilerplate
- Hard to understand the protocol

## Solution

A CLI tool to generate MCP server templates in seconds:
- **Python** support
- **12 templates** covering more scenarios
- **Minimal code** - just what you need

## Installation

```bash
pip install mcp-templates
```

## Usage

```bash
# Generate a database MCP server
mcp-templates new db-server --template database

# Generate an API MCP server
mcp-templates new api-server --template api

# Generate a file system MCP server
mcp-templates new fs-server --template filesystem

# Generate a GitHub MCP server
mcp-templates new github-server --template github

# Generate a Slack MCP server
mcp-templates new slack-server --template slack

# List available templates
mcp-templates list
```

## Templates (12 available)

### Core Templates
- **database** - SQLite database query tool
- **api** - REST API integration
- **filesystem** - File system operations

### Integration Templates
- **github** - GitHub API integration (issues, PRs, repos)
- **slack** - Slack messaging and channels
- **notion** - Notion workspace integration
- **twitter** - Twitter/X posting and search
- **email** - Email sending and reading (SMTP/IMAP)

### Utility Templates
- **calculator** - Mathematical calculations
- **weather** - Weather data from APIs
- **currency** - Currency conversion
- **translator** - Language translation

## Example: Create a database MCP server

```bash
$ mcp-templates new my-db --template database
Created: my-db/
  - main.py      # MCP server entry point
  - README.md    # Documentation
  - requirements.txt

$ cd my-db && pip install -r requirements.txt
$ python main.py
```

## Project Structure

```
mcp-templates/
├── main.py           # CLI entry point
├── generator.py      # Template generator
└── templates/         # Template files (12 templates)
    ├── database.py
    ├── api.py
    ├── filesystem.py
    ├── github.py
    ├── slack.py
    └── ...
```

## Next

- [ ] Add TypeScript support
- [ ] Add interactive prompts
- [ ] Add more cloud service templates

---
*Built: 2026-03-06*
*Updated: 2026-03-08 - Added 4 new templates*
