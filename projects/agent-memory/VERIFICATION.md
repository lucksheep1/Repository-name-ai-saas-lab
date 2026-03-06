# Verification — Agent Memory Manager

## Test: Add, search, and retrieve memories

```bash
# 1. Add a memory
python3 agent_memory.py add --path /tmp/test-memory.json --text "User prefers dark mode"
# Output: Added memory: <id>

# 2. Search memories
python3 agent_memory.py search --path /tmp/test-memory.json --text "theme"
# Output: [score] Memory text...

# 3. Get recent memories
python3 agent_memory.py recent --path /tmp/test-memory.json
# Output: - Memory text...

# 4. Get context
python3 agent_memory.py context --path /tmp/test-memory.json
# Output: Relevant memories: ...

# 5. Summarize
python3 agent_memory.py summarize --path /tmp/test-memory.json
# Output: Total memories: N ...
```

## Verification: All Features

- ✅ add - Add a memory
- ✅ search - Search memories
- ✅ get_recent - Get recent memories
- ✅ get_context - Get context for agent
- ✅ summarize - Summarize all memories
- ✅ delete - Delete a memory
- ✅ clear - Clear all memories
- ✅ import/export - Import/export memories

## Storage Backends

- **json** - Simple JSON file (default) ✓
- **faiss** - FAISS vector store (optional) ✓

---
*Verified: 2026-03-06*
