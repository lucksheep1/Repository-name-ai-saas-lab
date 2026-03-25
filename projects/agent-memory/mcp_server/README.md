# Agent Memory MCP Server

Exposes Agent Memory as a Model Context Protocol (MCP) server for integration with Claude Code, Cursor, Windsurf, and other AI IDEs.

## Quick Start

```bash
# Install dependencies
cd mcp_server
pip install -r requirements.txt

# Run server (reads JSON-RPC from stdin)
python server.py
```

## MCP Client Configuration

### For Claude Code / Cursor / Windsurf

Add to your MCP settings:

```json
{
  "mcpServers": {
    "agent-memory": {
      "command": "python",
      "args": ["projects/agent-memory/mcp_server/server.py"],
      "env": {
        "AGENT_MEMORY_PATH": "./memory.json"
      }
    }
  }
}
```

Or use the npx runner:

```bash
npx @modelcontextprotocol/server-filesystem ./projects/agent-memory
```

## Available Tools

| Tool | Description |
|------|-------------|
| `memory_add` | Add a new memory |
| `memory_search` | Search memories |
| `memory_get_recent` | Get recent memories |
| `memory_get_by_tag` | Get by tag |
| `memory_get_context` | Get condensed context |
| `memory_stats` | Get statistics |

## Example Usage

```python
# Via MCP protocol
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "memory_add", "arguments": {"text": "User prefers dark mode"}}, "id": 1}
```

## Status

🚀 **v3.2 Feature** - MCP Server Integration

---
*Added: 2026-03-25*