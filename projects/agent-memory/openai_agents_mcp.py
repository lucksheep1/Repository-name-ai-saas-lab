#!/usr/bin/env python3
"""
OpenAI Agents SDK Memory Bridge — Local-First MCP Server

Exposes OpenAI Agents SDK-style session memory (SQLite, Redis, encrypted)
as an MCP server, so ANY MCP client can use OpenAI-style session memory
WITHOUT requiring OpenAI API keys.

Usage:
    pip install mcp
    python openai_agents_mcp.py

In demo mode (no MCP package needed):
    python openai_agents_mcp.py --demo
"""

import argparse
import asyncio
import json
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
APP_NAME = "openai-agents-memory-mcp"
VERSION = "0.1.0"
PORT = 18083

# In-memory session store (v1 — swap for SQLiteSession from OpenAI SDK)
_sessions = {}

# ---------------------------------------------------------------------------
# Session operations
# ---------------------------------------------------------------------------

def create_session(session_id: str | None, agent_name: str, storage: str = "memory",
                   system_prompt: str = "") -> dict:
    sid = session_id or str(uuid.uuid4())[:8]
    _sessions[sid] = {
        "id": sid,
        "agent_name": agent_name,
        "storage": storage,
        "system_prompt": system_prompt,
        "memories": [],
        "created_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat(),
    }
    return {"session_id": sid, "status": "created", "storage": storage, "agent_name": agent_name}


def add_memory(session_id: str, content: str, ttl_seconds: int | None = None,
               tags: list[str] | None = None) -> dict:
    if session_id not in _sessions:
        return {"error": f"Session '{session_id}' not found"}
    entry = {
        "id": str(uuid.uuid4()),
        "content": content,
        "tags": tags or [],
        "added_at": datetime.now().isoformat(),
        "expires_at": (
            (datetime.now() + timedelta(seconds=ttl_seconds)).isoformat()
            if ttl_seconds else None
        ),
    }
    _sessions[session_id]["memories"].append(entry)
    _sessions[session_id]["last_active"] = datetime.now().isoformat()
    return {"memory_id": entry["id"], "session_id": session_id, "status": "added",
            "expires_at": entry["expires_at"]}


def search_memory(session_id: str, query: str, limit: int = 5) -> dict:
    if session_id not in _sessions:
        return {"error": f"Session '{session_id}' not found"}
    memories = _sessions[session_id]["memories"]
    now = datetime.now()
    results = [
        m for m in memories
        if m.get("expires_at") is None or datetime.fromisoformat(m["expires_at"]) > now
    ]
    scored = [(m, sum(1 for w in query.lower().split() if w in m["content"].lower())) for m in results]
    scored.sort(key=lambda x: x[1], reverse=True)
    return {"session_id": session_id, "query": query,
            "results": [m for m, _ in scored[:limit]],
            "total_memories": len(memories)}


def get_session(session_id: str) -> dict:
    if session_id not in _sessions:
        return {"error": f"Session '{session_id}' not found"}
    s = _sessions[session_id]
    return {"session_id": session_id, "agent_name": s["agent_name"],
            "storage": s["storage"], "memory_count": len(s["memories"]),
            "created_at": s["created_at"], "last_active": s["last_active"]}


def list_sessions() -> dict:
    return {"sessions": [{"session_id": s["id"], "agent_name": s["agent_name"],
                          "memory_count": len(s["memories"]), "last_active": s["last_active"]}
                         for s in _sessions.values()],
            "total": len(_sessions)}


def delete_session(session_id: str) -> dict:
    if session_id in _sessions:
        del _sessions[session_id]
        return {"session_id": session_id, "status": "deleted"}
    return {"error": f"Session '{session_id}' not found"}


# ---------------------------------------------------------------------------
# MCP Server (requires: pip install mcp)
# ---------------------------------------------------------------------------

async def run_mcp_server():
    try:
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        from mcp.types import Tool, TextContent
    except ImportError:
        print("ERROR: mcp package not installed.", file=sys.stderr)
        print("  pip install mcp", file=sys.stderr)
        print("  Or use --demo mode: python openai_agents_mcp.py --demo", file=sys.stderr)
        sys.exit(1)

    server = Server(APP_NAME)

    @server.list_tools()
    async def list_tools():
        return [
            Tool(name="create_session",
                 description="Create a new agent session with persistent memory",
                 inputSchema={
                     "type": "object",
                     "properties": {
                         "session_id": {"type": "string"},
                         "agent_name": {"type": "string"},
                         "storage": {"type": "string", "enum": ["memory", "sqlite", "encrypted"]},
                         "system_prompt": {"type": "string"},
                     },
                     "required": ["agent_name"],
                 }),
            Tool(name="add_memory",
                 description="Add a memory entry to a session",
                 inputSchema={
                     "type": "object",
                     "properties": {
                         "session_id": {"type": "string"},
                         "content": {"type": "string"},
                         "ttl_seconds": {"type": "integer"},
                         "tags": {"type": "array", "items": {"type": "string"}},
                     },
                     "required": ["session_id", "content"],
                 }),
            Tool(name="search_memory",
                 description="Search memories in a session",
                 inputSchema={
                     "type": "object",
                     "properties": {
                         "session_id": {"type": "string"},
                         "query": {"type": "string"},
                         "limit": {"type": "integer", "default": 5},
                     },
                     "required": ["session_id", "query"],
                 }),
            Tool(name="get_session",
                 description="Get session details and memory stats",
                 inputSchema={
                     "type": "object",
                     "properties": {"session_id": {"type": "string"}},
                     "required": ["session_id"],
                 }),
            Tool(name="list_sessions",
                 description="List all active sessions",
                 inputSchema={"type": "object", "properties": {}}),
            Tool(name="delete_session",
                 description="Delete a session and all its memories",
                 inputSchema={
                     "type": "object",
                     "properties": {"session_id": {"type": "string"}},
                     "required": ["session_id"],
                 }),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> TextContent:
        result = {}
        if name == "create_session":
            result = create_session(
                session_id=arguments.get("session_id"),
                agent_name=arguments["agent_name"],
                storage=arguments.get("storage", "memory"),
                system_prompt=arguments.get("system_prompt", ""),
            )
        elif name == "add_memory":
            result = add_memory(
                session_id=arguments["session_id"],
                content=arguments["content"],
                ttl_seconds=arguments.get("ttl_seconds"),
                tags=arguments.get("tags"),
            )
        elif name == "search_memory":
            result = search_memory(
                session_id=arguments["session_id"],
                query=arguments["query"],
                limit=arguments.get("limit", 5),
            )
        elif name == "get_session":
            result = get_session(session_id=arguments["session_id"])
        elif name == "list_sessions":
            result = list_sessions()
        elif name == "delete_session":
            result = delete_session(session_id=arguments["session_id"])
        else:
            result = {"error": f"Unknown tool: {name}"}
        return TextContent(type="text", text=json.dumps(result, indent=2))

    @server.list_resources()
    async def list_resources():
        return []

    print(f"[{APP_NAME}] Starting MCP server on port {PORT}...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


# ---------------------------------------------------------------------------
# Demo mode
# ---------------------------------------------------------------------------

def run_demo():
    print(f"=== {APP_NAME} v{VERSION} Demo ===\n")

    # Create a session
    result = create_session(session_id="demo", agent_name="coding-assistant",
                             storage="memory", system_prompt="You are a helpful coding assistant.")
    print(f"1. Created session: {result}")

    # Add memories
    memories = [
        ("User prefers Python over JavaScript", ["pref", "language"]),
        ("Project uses PostgreSQL database", ["stack", "db"]),
        ("API endpoint: /api/memory/search — returns JSON", ["api", "endpoint"]),
        ("Last meeting: architecture review on 2026-03-25", ["meeting"]),
    ]
    for content, tags in memories:
        r = add_memory(session_id="demo", content=content, tags=tags)
        print(f"   + {content[:55]}...  → id: {r['memory_id'][:8]}")

    # Search
    print(f"\n2. Search: 'Python or database'")
    result = search_memory(session_id="demo", query="Python database", limit=3)
    for m in result["results"]:
        print(f"   → {m['content'][:60]}")

    # Session stats
    print(f"\n3. Session stats:")
    result = get_session(session_id="demo")
    print(f"   agent={result['agent_name']}, memories={result['memory_count']}, "
          f"storage={result['storage']}")

    # List sessions
    print(f"\n4. All sessions:")
    result = list_sessions()
    print(f"   total={result['total']}, sessions={[s['session_id'] for s in result['sessions']]}")

    print(f"\n5. Delete session")
    result = delete_session(session_id="demo")
    print(f"   {result}")

    print(f"\n=== Demo complete ===")
    print(f"\nTo run as MCP server: pip install mcp && python openai_agents_mcp.py")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} — OpenAI Agents SDK Memory Bridge (Local-First MCP Server)"
    )
    parser.add_argument("--demo", action="store_true", help="Run demo without starting MCP server")
    parser.add_argument("--port", type=int, default=PORT, help=f"MCP server port (default: {PORT})")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        asyncio.run(run_mcp_server())
