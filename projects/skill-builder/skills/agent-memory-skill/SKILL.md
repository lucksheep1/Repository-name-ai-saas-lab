---
name: agent-memory-skill
description: Manage persistent memory for AI agents using Model Context Protocol. Store, search, and recall information across sessions. MCP-native: exposes memory_search, memory_add, memory_get, memory_list, memory_clear tools. Supports TTL expiration, AES encryption, tagging, and multiple storage backends (JSON/SQLite/Redis). Use when: building AI agents that need memory, working with Cursor/Claude Code/OpenClaw MCP integration, or needing persistent context across conversations.
---

# Agent Memory Skill

## When to Use

Use this skill when the user mentions: memory, remember, recall, persist, context, mcp memory, agent memory.


## SENSITIVE DATA

No sensitive data stored by default. User memory is stored locally. Encryption available via --encryption-key flag.

## Session Start

Check workspace for existing memory store (memory.json, memory.db). Report memory count on startup.

## Commands

- `add <text>` — store a memory with optional TTL (e.g. '1h', '7d')
- `search <query>` — find relevant memories
- `list` — show recent memories
- `clear [--all]` — clear memories

## Quality Standards

- Always verify destructive operations before executing
- Report progress clearly during long-running tasks
- Mask all sensitive data in output
- Maintain context between commands in a session
