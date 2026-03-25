#!/usr/bin/env python3
"""
MCP Server Demo - Interactive demo showing MCP tools in action.

This simulates what Claude Desktop would do when calling our MCP server.
"""

import json
import sys
sys.path.insert(0, '.')

from mcp_server.server import AgentMemoryMCPServer

def demo():
    server = AgentMemoryMCPServer()
    
    print("=" * 60)
    print("🎯 Agent Memory MCP Server Demo")
    print("=" * 60)
    
    # Step 1: List tools
    print("\n📋 Step 1: List available tools")
    result = server.handle_request("tools/list")
    for tool in result["tools"]:
        print(f"  • {tool['name']}: {tool['description'][:50]}...")
    
    # Step 2: Add memories
    print("\n➕ Step 2: Add sample memories")
    memories = [
        {"text": "User prefers dark mode in IDE", "tags": ["preference", "ui"]},
        {"text": "Working on Python MCP server project", "tags": ["project", "mcp"]},
        {"text": "Remember to document the API", "tags": ["todo", "docs"]},
    ]
    for m in memories:
        result = server.handle_request("tools/call", {
            "name": "memory_add",
            "arguments": m
        })
        print(f"  ✓ Added: {m['text'][:40]}...")
    
    # Step 3: Search
    print("\n🔍 Step 3: Search for 'dark mode'")
    result = server.handle_request("tools/call", {
        "name": "memory_search",
        "arguments": {"query": "dark mode", "top_k": 3}
    })
    results = json.loads(result["content"][0]["text"])
    for r in results:
        print(f"  • {r['text'][:50]}...")
    
    # Step 4: Get context
    print("\n📝 Step 4: Get agent context (max 500 tokens)")
    result = server.handle_request("tools/call", {
        "name": "memory_get_context",
        "arguments": {"max_tokens": 500, "max_memories": 5}
    })
    context = result["content"][0]["text"]
    print(f"  {context[:200]}...")
    
    # Step 5: Statistics
    print("\n📊 Step 5: Memory statistics")
    result = server.handle_request("tools/call", {
        "name": "memory_stats",
        "arguments": {}
    })
    stats = json.loads(result["content"][0]["text"])
    print(f"  Total memories: {stats['total']}")
    print(f"  Recent (last 100): {stats['recent']}")
    
    # Step 6: Timeline
    print("\n📅 Step 6: Timeline view")
    result = server.handle_request("tools/call", {
        "name": "memory_timeline",
        "arguments": {"limit": 5}
    })
    timeline = json.loads(result["content"][0]["text"])
    for t in timeline:
        created = t.get('created', '')[:19]
        print(f"  • {created} | {t['text'][:40]}...")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete! MCP server is ready for Claude Desktop.")
    print("=" * 60)

if __name__ == "__main__":
    demo()