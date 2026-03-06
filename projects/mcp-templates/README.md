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
- **Multiple templates** (database, API, file system)
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

# List available templates
mcp-templates list
```

## Templates

### database
Simple database query tool with SQLite support.

### api
REST API integration with configurable endpoints.

### filesystem
File system operations (read, write, list).

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
└── templates/         # Template files
    ├── database.py
    ├── api.py
    └── filesystem.py
```

## Next

- [ ] Add more templates (GitHub, Slack, etc.)
- [ ] Add TypeScript support
- [ ] Add interactive prompts

---
*Built: 2026-03-06*
