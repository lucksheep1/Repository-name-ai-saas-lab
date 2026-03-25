#!/usr/bin/env python3
"""Test MCP Server handlers without JSON-RPC transport."""

import json
import sys
sys.path.insert(0, '.')

from mcp_server.server import AgentMemoryMCPServer

def test():
    server = AgentMemoryMCPServer()
    
    # Test initialize
    result = server.handle_request("initialize")
    assert result["serverInfo"]["name"] == "agent-memory"
    print("✓ initialize OK")
    
    # Test tools/list
    result = server.handle_request("tools/list")
    assert "tools" in result
    tool_names = [t["name"] for t in result["tools"]]
    assert "memory_add" in tool_names
    print(f"✓ tools/list OK ({len(tool_names)} tools)")
    
    # Test memory_add
    result = server.handle_request("tools/call", {
        "name": "memory_add",
        "arguments": {"text": "Test memory from MCP test"}
    })
    assert "content" in result
    print("✓ memory_add OK")
    
    # Test memory_search
    result = server.handle_request("tools/call", {
        "name": "memory_search",
        "arguments": {"query": "test", "top_k": 3}
    })
    assert "content" in result
    print("✓ memory_search OK")
    
    # Test memory_stats
    result = server.handle_request("tools/call", {
        "name": "memory_stats",
        "arguments": {}
    })
    assert "content" in result
    stats = json.loads(result["content"][0]["text"])
    print(f"✓ memory_stats OK (total: {stats['total']})")
    
    print("\n✅ All MCP Server tests passed!")

if __name__ == "__main__":
    test()