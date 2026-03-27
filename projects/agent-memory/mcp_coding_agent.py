#!/usr/bin/env python3
"""
agent-memory MCP server for AI coding agents (Claude Code, Cursor, etc.)

Extends the base MCP server with coding-specific memory tools:
- project_context: Store and recall project structure, patterns, conventions
- code_facts: Remember facts about the codebase
- architectural_decisions: Track ADR-style decisions
- session_resume: Resume work across sessions

Usage:
    python mcp_coding_agent.py [--storage json|sqlite|redis]
    # Then connect via MCP client (Claude Code, Cursor, etc.)
"""

import argparse
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from agent_memory import Memory


def create_app(storage="json", path="./coding_memory.json", ttl=None, encryption_key=None):
    """Create the coding agent memory MCP application."""
    memory = Memory(storage=storage, path=path, ttl=ttl, encryption_key=encryption_key)

    def tool_memory_project_add(text: str, project: str = None, tags: list = None) -> dict:
        """Add a project context memory.
        
        Use when: learning project structure, conventions, patterns.
        Tags: architecture, convention, pattern, structure, setup, config.
        """
        tags = tags or []
        if project:
            tags = list(set(tags + [project]))
        memory.add(text, metadata={"source": "project_context", "category": "project", "tags": tags})
        return {"status": "ok", "message": "Project context added"}

    def tool_memory_code_fact(text: str, entity: str = None, tags: list = None) -> dict:
        """Store a code fact about the codebase.
        
        Use when: remembering function purposes, API shapes, DB schemas, configs.
        Example: "User model is in models/user.py with fields: id, email, role"
        """
        tags = tags or []
        if entity:
            tags = list(set(tags + ["entity:" + entity]))
        memory.add(text, metadata={"source": "code_fact", "category": "fact", "tags": tags})
        return {"status": "ok", "message": "Code fact stored"}

    def tool_memory_decision(text: str, decision_type: str = None, status: str = "accepted") -> dict:
        """Record an architectural decision (ADR style).
        
        Use when: making design choices, selecting libraries, defining patterns.
        status: proposed | accepted | deprecated | superseded
        """
        memory.add(
            text,
            metadata={
                "source": "adr",
                "category": "decision",
                "decision_type": decision_type or "general",
                "status": status,
            }
        )
        return {"status": "ok", "message": f"Decision recorded ({status})"}

    def tool_memory_search(query: str, category: str = None, limit: int = 10) -> dict:
        """Search coding memory by query.
        
        Returns most relevant memories matching the query.
        """
        results = memory.search(query, top_k=limit)
        if category:
            results = [r for r in results if r.get("metadata", {}).get("category") == category]
        return {
            "query": query,
            "count": len(results),
            "results": [
                {
                    "id": r.get("id"),
                    "text": r.get("text", "")[:200],
                    "category": r.get("metadata", {}).get("category"),
                    "tags": r.get("metadata", {}).get("tags", []),
                }
                for r in results
            ],
        }

    def tool_memory_session_resume(project: str = None) -> dict:
        """Get all relevant context for resuming work on a project.
        
        Returns: recent decisions, code facts, project patterns for this project.
        """
        query = project or ""
        results = memory.search(query, top_k=50)
        
        decisions = [
            {"text": r.get("text", ""), "status": r.get("metadata", {}).get("status")}
            for r in results
            if r.get("metadata", {}).get("category") == "decision"
        ]
        facts = [
            {"text": r.get("text", "")[:200], "entity": r.get("metadata", {}).get("source")}
            for r in results
            if r.get("metadata", {}).get("category") == "fact"
        ]
        patterns = [
            {"text": r.get("text", "")[:200], "tags": r.get("metadata", {}).get("tags", [])}
            for r in results
            if r.get("metadata", {}).get("category") == "project"
        ]
        return {
            "decisions": decisions[:10],
            "facts": facts[:20],
            "patterns": patterns[:20],
            "total": len(decisions) + len(facts) + len(patterns),
        }

    def tool_memory_list(category: str = None, limit: int = 20) -> dict:
        """List recent memories, optionally filtered by category."""
        memories = memory.memories
        if category:
            memories = [m for m in memories if m.get("metadata", {}).get("category") == category]
        memories = sorted(memories, key=lambda m: m.get("created_at", ""), reverse=True)[:limit]
        return {
            "count": len(memories),
            "memories": [
                {
                    "id": m.get("id"),
                    "text": m.get("text", "")[:200],
                    "category": m.get("metadata", {}).get("category"),
                    "created": m.get("created_at", ""),
                }
                for m in memories
            ],
        }

    def tool_memory_stats() -> dict:
        """Get memory statistics for the current project."""
        memories = memory.memories
        total = len(memories)
        categories = {}
        for m in memories:
            cat = m.get("metadata", {}).get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        return {
            "total": total,
            "categories": categories,
            "storage": storage,
        }

    tools = [
        {
            "name": "memory_project_add",
            "description": "Add project context: structure, conventions, patterns. Use when learning a new codebase or making architectural changes.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Project context to remember"},
                    "project": {"type": "string", "description": "Project name (optional)"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags: architecture, convention, pattern, etc."},
                },
                "required": ["text"],
            },
        },
        {
            "name": "memory_code_fact",
            "description": "Store a code fact: function purpose, API shape, schema, config. Example: 'UserService.get_by_id() returns User or None'.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Code fact to remember"},
                    "entity": {"type": "string", "description": "Entity name (e.g. 'UserService', 'UserModel')"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["text"],
            },
        },
        {
            "name": "memory_decision",
            "description": "Record an architectural decision (ADR style). Use when making design choices: library selection, pattern adoption, architecture changes.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Decision text (e.g. 'Use PostgreSQL for user data, Redis for sessions')"},
                    "decision_type": {"type": "string", "description": "Type: database, library, architecture, pattern, other"},
                    "status": {"type": "string", "description": "Status: proposed, accepted, deprecated, superseded"},
                },
                "required": ["text"],
            },
        },
        {
            "name": "memory_search",
            "description": "Search coding memories. Returns relevant project context, code facts, and decisions.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "category": {"type": "string", "description": "Filter by category: project, fact, decision"},
                    "limit": {"type": "integer", "description": "Max results (default 10)"},
                },
                "required": ["query"],
            },
        },
        {
            "name": "memory_session_resume",
            "description": "Get all context needed to resume work on a project. Returns recent decisions, code facts, and patterns.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Project name (optional)"},
                },
            },
        },
        {
            "name": "memory_list",
            "description": "List recent memories, optionally filtered by category.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Filter: project, fact, decision"},
                    "limit": {"type": "integer", "description": "Max results (default 20)"},
                },
            },
        },
        {
            "name": "memory_stats",
            "description": "Get memory statistics: total count, breakdown by category.",
            "input_schema": {"type": "object", "properties": {}},
        },
    ]

    return {
        "memory": memory,
        "tools": tools,
        "handlers": {
            "memory_project_add": tool_memory_project_add,
            "memory_code_fact": tool_memory_code_fact,
            "memory_decision": tool_memory_decision,
            "memory_search": tool_memory_search,
            "memory_session_resume": tool_memory_session_resume,
            "memory_list": tool_memory_list,
            "memory_stats": tool_memory_stats,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="agent-memory MCP server for AI coding agents")
    parser.add_argument("--storage", default="json", choices=["json", "sqlite", "redis"])
    parser.add_argument("--path", default="./coding_memory.json")
    parser.add_argument("--ttl", default=None)
    parser.add_argument("--encryption-key", default=None)
    parser.add_argument("--port", type=int, default=18082)
    args = parser.parse_args()

    print(f"agent-memory MCP for AI Coding Agents")
    print(f"  Storage: {args.storage}")
    print(f"  Path: {args.path}")
    print(f"  Port: {args.port}")
    print()
    print("Available MCP tools:")
    
    app = create_app(
        storage=args.storage,
        path=args.path,
        ttl=args.ttl,
        encryption_key=args.encryption_key,
    )
    
    for tool in app["tools"]:
        print(f"  {tool['name']}")
    
    print()
    print("Connect via MCP client (Claude Code, Cursor, etc.)")
    print("Or run: python -m agent_memory.mcp_server")
    print()
    print("Coding-specific tools:")
    print("  memory_project_add  — Learn project structure/conventions")
    print("  memory_code_fact   — Store API shapes, schemas, configs")
    print("  memory_decision    — Record architectural decisions (ADR)")
    print("  memory_search      — Search coding memories")
    print("  memory_session_resume — Resume work on a project")
    print("  memory_list        — List recent memories")
    print("  memory_stats       — Show memory statistics")


if __name__ == "__main__":
    main()
