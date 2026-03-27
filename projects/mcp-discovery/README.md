# MCP Discovery

CLI tool to discover and analyze MCP servers from npm registry.

## Problem

Finding the right MCP server for your AI agent is hard. No easy way to search and compare.

## Solution

Search npm registry for MCP servers, analyze details.

## Installation

```bash
cd projects/mcp-discovery
python3 cli.py --help
```

## Usage

```bash
# Search for MCP servers
python3 cli.py "mcp server"
python3 cli.py "@modelcontextprotocol"

# Analyze specific package
python3 cli.py --analyze "@modelcontextprotocol/server-everything"
```

## Example Output

```
🔍 Searching npm for '@modelcontextprotocol'...

📦 Found 15 packages:

1. figma-mcp (0.1.4)
   ModelContextProtocol server for Figma...

2. @modelcontextprotocol/sdk (1.28.0)
   Model Context Protocol implementation for TypeScript...
```

## Verification

- ✅ Searches npm registry
- ✅ Analyzes package details
- ✅ Shows repo URLs
