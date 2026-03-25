# Agent Memory MCP Server

A JSON-RPC based MCP server that exposes Agent Memory as tools for AI IDEs like Claude Desktop, Cursor, and Windsurf.

![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## Features

- 🔌 **MCP Protocol** - Compliant with MCP 2024-11-05
- 🧠 **9 Tools** - Full CRUD operations for memories
- ⚡ **Zero Dependencies** - Uses core agent-memory only
- 🖥️ **Claude Desktop** - Ready to use integration
- 🧪 **Tested** - Demo script included

## Installation

```bash
pip install agent-memory

# Or from source
cd projects/agent-memory
pip install -e .
```

## Quick Start

```bash
# Run the demo
python -m agent_memory.mcp_server.demo

# Or start the server
python -m agent_memory.mcp_server.server
```

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `memory_add` | Add a memory | `text`, `ttl?`, `tags?`, `encrypt?` |
| `memory_search` | Search memories | `query`, `top_k?` |
| `memory_get_recent` | Get recent | `limit?` |
| `memory_get_by_tag` | Filter by tag | `tag` |
| `memory_get_context` | Get context | `max_tokens?`, `max_memories?` |
| `memory_stats` | Statistics | - |
| `memory_delete` | Delete by ID | `memory_id` |
| `memory_timeline` | Timeline view | `limit?` |
| `memory_export` | Export JSON | `filepath` |

## Claude Desktop Integration

See [mcp-claude-desktop.md](docs/mcp-claude-desktop.md) for setup instructions.

```json
{
  "mcpServers": {
    "agent-memory": {
      "command": "python3",
      "args": ["/path/to/mcp_server/server.py"]
    }
  }
}
```

## Example Usage

```python
# Via MCP JSON-RPC
{"jsonrpc": "2.0", "method": "tools/call", "params": {
  "name": "memory_add",
  "arguments": {"text": "User prefers dark mode", "tags": ["preference"]}
}, "id": 1}
```

## Status

🚀 v3.2 Released - MCP Server Integration

---
*2026-03-25*