# Agent Context Manager

Lightweight context management for AI agents across sessions.

## Problem

Agents lose context between sessions. Existing solutions:
- Too complex (LangChain memory)
- No persistence
- Coupled to specific frameworks

## Solution

A simple, standalone context manager:
- **Multi-session**: Track context across sessions
- **Persistent**: SQLite-backed storage
- **Lightweight**: Single Python file, no heavy dependencies
- **Flexible**: Works with any agent/framework
- **Priority & Tags**: Organize memories by importance
- **Export**: JSON and Markdown export

## Installation

```bash
pip install agent-context-manager
```

## Usage

```python
from context_manager import ContextManager

# Initialize (creates SQLite db in current directory)
ctx = ContextManager("my-agent")

# Add to context
ctx.add("User prefers Python over JavaScript")
ctx.add("Working on authentication feature", priority=5)

# Add with tags
ctx.add_with_priority("Bug in login", priority=5, session_id="session-123", tags="bug,urgent")

# Get context for next turn
context = ctx.get_context(max_tokens=2000)
print(context)

# List all memories
memories = ctx.list_memories()
for m in memories:
    print(f"- {m['content']} ({m['created_at']})")

# Get by session
session_memories = ctx.get_by_session("session-123")

# Get by priority
important = ctx.get_by_priority(min_priority=4)

# Get statistics
stats = ctx.get_stats()
print(f"Total: {stats['total_memories']}, Sessions: {stats['unique_sessions']}")

# Export to JSON
ctx.export_json("backup.json")

# Export to Markdown
ctx.export_markdown("context.md")

# Clear old context
ctx.clear_older_than(days=7)
```

## CLI

```bash
# Add a memory
context-manager add "User likes dark mode"

# List memories
context-manager list

# Search
context-manager search "preferences"

# Get statistics
context-manager stats

# Export to JSON
context-manager export

# Export to Markdown
context-manager export --markdown

# List sessions
context-manager sessions

# Clear old memories
context-manager clear --days 7

# Clear all
context-manager clear --all
```

## Features

- SQLite-backed persistence
- Session tracking
- Priority system (1-5)
- Tag support
- Search functionality
- Statistics dashboard
- JSON export
- Markdown export
- Session filtering

## How It Works

1. **SQLite storage**: Persistent across restarts
2. **Token counting**: Estimate context size
3. **Time-based cleanup**: Auto-remove old memories
4. **Priority retrieval**: Get important memories first

## Score

- Utility: 9/10
- Innovation: 7/10
- Simplicity: 9/10
- Reusability: 9/10
- Market: 8/10

**Total: 42/50**

## Next

- [ ] Add embedding-based search
- [ ] Add MCP server wrapper
- [ ] Add summarization

---
*Built: 2026-03-06*
*Updated: 2026-03-08 - Added export features*
