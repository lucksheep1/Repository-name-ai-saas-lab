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
ctx.add("Working on authentication feature")

# Get context for next turn
context = ctx.get_context(max_tokens=2000)
print(context)

# List all memories
memories = ctx.list_memories()
for m in memories:
    print(f"- {m['content']} ({m['created_at']})")

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

# Clear old
context-manager clear --days 7
```

## How It Works

1. **SQLite storage**: Persistent across restarts
2. **Token counting**: Estimate context size
3. **Time-based cleanup**: Auto-remove old memories

## Score

- Utility: 8/10
- Innovation: 5/10 (based on Engram pattern)
- Simplicity: 9/10
- Reusability: 8/10
- Market: 6/10

**Total: 36/50**

## Next

- [ ] Add embedding-based search
- [ ] Add MCP server wrapper
- [ ] Add summarization

---
*Built: 2026-03-06*
