---
name: agent-memory-ops
description: Manage persistent memory for AI agents. Store, search, and recall information across sessions. Supports TTL expiration, encryption, tagging, and multiple storage backends (JSON/SQLite/Redis). Use when: the user wants to remember something across conversations, search past information, set time-based memory expiration, encrypt sensitive data, or manage knowledge bases.
---

# Agent Memory Ops

## When to Use

Use this skill when the user mentions: remember, recall, forget, search memory, what do you know, memory, persist.


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
