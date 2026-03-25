# Agent Memory - Claude Desktop Integration

## Quick Setup

1. Find your Claude Desktop config location:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add this to your config:

```json
{
  "mcpServers": {
    "agent-memory": {
      "command": "python3",
      "args": [
        "/path/to/projects/agent-memory/mcp_server/server.py"
      ],
      "env": {
        "AGENT_MEMORY_PATH": "/path/to/projects/agent-memory/memory.json"
      }
    }
  }
}
```

Replace `/path/to/` with the actual absolute path to your workspace.

3. Restart Claude Desktop

## Available Tools

Once connected, you'll see these tools:

- **memory_add** - Add a memory with optional TTL/tags
- **memory_search** - Search memories
- **memory_get_recent** - Get recent memories
- **memory_get_by_tag** - Filter by tag
- **memory_get_context** - Get condensed context
- **memory_stats** - Get statistics

## Example Prompts

```
"Remember that I prefer dark mode in VS Code"
"Search my memory for anything about Python"
"What's my recent context?"
"Show me memories tagged project"
```

## Troubleshooting

**Connection refused**
- Check Python path is correct
- Verify the path to server.py exists
- Check logs at: `~/Library/Logs/Claude/`

---
*2026-03-25*