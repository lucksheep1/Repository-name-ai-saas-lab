# Agent Memory - Deep Integration Demo

A full demo showing all features working together: core lib + MCP server + dashboard.

## Running the Demo

```bash
# From projects/agent-memory directory
python -m mcp_server.demo
```

This demonstrates:
1. MCP Server 9 tools working
2. Memory CRUD operations
3. Search and context generation
4. Timeline view

## API Test

```bash
# Test MCP server directly
echo '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}' | python3 mcp_server/server.py
```

## Next: Add streaming context

---
*2026-03-25*