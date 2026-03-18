#!/usr/bin/env python3
"""
Agent Memory - MCP Server
==========================
A Model Context Protocol (MCP) server for agent-memory.

This allows AI assistants (Claude, GPT, etc.) to use agent-memory
as a persistent memory layer via MCP protocol.

Usage:
    pip install mcp
    python mcp_server.py
    
    # Configure in your MCP client
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any
from agent_memory import Memory

# Initialize memory
memory = Memory(storage="json", path="./memory.json")


def add_memory(text: str, tags: list = None, metadata: dict = None) -> dict:
    """Add a new memory."""
    if tags:
        memory_id = memory.add_with_tags(text, tags=tags, metadata=metadata)
    else:
        memory_id = memory.add(text, metadata=metadata)
    return {"id": memory_id, "status": "added"}


def search_memories(query: str, top_k: int = 5) -> dict:
    """Search memories."""
    results = memory.search(query, top_k=top_k)
    return {"results": results, "count": len(results)}


def get_context(max_tokens: int = 2000) -> dict:
    """Get context for an agent."""
    context = memory.get_context(max_tokens=max_tokens)
    return {"context": context}


def get_timeline(limit: int = 20) -> dict:
    """Get timeline of memories."""
    timeline = memory.get_timeline(limit=limit)
    return {"timeline": timeline}


def get_recent(limit: int = 10) -> dict:
    """Get recent memories."""
    recent = memory.get_recent(limit=limit)
    return {"memories": recent, "count": len(recent)}


def get_by_tag(tag: str) -> dict:
    """Get memories by tag."""
    results = memory.get_by_tag(tag)
    return {"results": results, "count": len(results)}


def get_stats() -> dict:
    """Get memory statistics."""
    return {
        "count": memory.count(),
        "tags": list(set(
            tag 
            for mem in memory.get_recent(limit=100) 
            for tag in mem.get("tags", [])
        )),
    }


# MCP Protocol handlers (simplified)
def handle_request(method: str, params: dict = None) -> dict:
    """Handle MCP request."""
    params = params or {}
    
    handlers = {
        "add": lambda: add_memory(
            params.get("text", ""),
            params.get("tags"),
            params.get("metadata")
        ),
        "search": lambda: search_memories(
            params.get("query", ""),
            params.get("top_k", 5)
        ),
        "context": lambda: get_context(params.get("max_tokens", 2000)),
        "timeline": lambda: get_timeline(params.get("limit", 20)),
        "recent": lambda: get_recent(params.get("limit", 10)),
        "by_tag": lambda: get_by_tag(params.get("tag", "")),
        "stats": get_stats,
    }
    
    handler = handlers.get(method)
    if handler:
        return {"success": True, "data": handler()}
    return {"success": False, "error": f"Unknown method: {method}"}


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Memory MCP Server")
    parser.add_argument("command", choices=["add", "search", "context", "timeline", "recent", "by_tag", "stats"])
    parser.add_argument("--text", help="Text to add or search query")
    parser.add_argument("--tag", help="Tag to filter by")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--limit", type=int, default=10, help="Limit results")
    parser.add_argument("--max-tokens", type=int, default=2000, help="Max tokens for context")
    parser.add_argument("--tags", help="Comma-separated tags")
    
    args = parser.parse_args()
    
    params = {}
    if args.text:
        params["text"] = args.text
    if args.tag:
        params["tag"] = args.tag
    if args.tags:
        params["tags"] = args.tags.split(",")
    params["top_k"] = args.top_k
    params["limit"] = args.limit
    params["max_tokens"] = args.max_tokens
    
    result = handle_request(args.command, params)
    import json
    print(json.dumps(result, indent=2))
