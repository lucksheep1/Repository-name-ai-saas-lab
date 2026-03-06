# Verification — Agent Context Manager

## Test: Add, list, search, and clear memories

```bash
# 1. Add a memory
python3 context_manager.py add "User prefers dark mode"
# Output: ✓ Memory added

# 2. List memories
python3 context_manager.py list
# Output: [timestamp] Memory content

# 3. Search memories
python3 context_manager.py search "preferences"
# Output: [timestamp] Memory content

# 4. Clear old memories
python3 context_manager.py clear --days 7
# Output: ✓ Cleared N memories older than 7 days
```

## Verification: All Features

- ✅ add - Add a memory
- ✅ list - List all memories
- ✅ search - Search memories
- ✅ clear - Clear old memories

## Storage

- SQLite database (default_context.db) ✓
- Persistent across restarts ✓

## Usage

```python
from context_manager import ContextManager

# Initialize
ctx = ContextManager("my-agent")

# Add memory
ctx.add("User preferences")

# Get context
context = ctx.get_context(max_tokens=2000)

# List memories
memories = ctx.list_memories()

# Clear old
ctx.clear_older_than(days=7)
```

---
*Verified: 2026-03-06*
