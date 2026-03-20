# Agent Memory v3.1: TTL Implementation Draft

## Overview
Implement Time-To-Live (TTL) support for automatic memory expiration.

## Motivation
- Users need automatic cleanup of old session data
- Prevent memory bloat from accumulating stale data
- Align with LangChain feature requests

## Proposed Interface

```python
from agent_memory import Memory

# Default TTL (7 days)
memory = Memory(ttl="7d")

# Per-key TTL
memory.add("temp_data", {"key": "value"}, ttl="1h")

# Check remaining TTL
remaining = memory.ttl("temp_data")

# Disable TTL for specific keys
memory.add("permanent", {"data": "value"}, ttl=None)
```

## Implementation Details

### TTL Format Support
- `s` - seconds
- `m` - minutes  
- `h` - hours
- `d` - days
- `w` - weeks

### Storage Backends
- In-memory: Track expiry in metadata dict
- Redis: Use native TTL commands (SETEX)
- SQLite: Store expiry timestamp, cleanup on read

### Edge Cases
- Expired keys return None/raise exception
- TTL=0 means immediate expiration
- TTL=None means never expire

## Success Criteria
- [ ] TTL format parsing works
- [ ] Automatic expiration on read
- [ ] Background cleanup task
- [ ] Redis backend TTL support
- [ ] Unit tests pass

---
*Draft created by AI SaaS Lab - 2026-03-20*
