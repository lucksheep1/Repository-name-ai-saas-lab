# Feature: Redis Backend

## Status: ✅ Implemented in v3.1.0

## Quick Start

```python
from agent_memory import Memory

# Redis backend
m = Memory(
    storage="redis",
    redis_url="redis://localhost:6379",
    ttl="30m"
)

m.add("session data", ttl="1h")
m.add("cache", ttl="5m", encrypt=True)
```

## Features

- **Native TTL**: Redis `SETEX` for automatic expiration
- **Encryption**: Optional Fernet encryption
- **Graceful Fallback**: Works without Redis available
- **Same API**: All operations work identically to JSON/SQLite backends

## Environment Variables

```bash
# Optional environment configuration via cli.py
AGENT_MEMORY_PATH=./memory.json  # path for json/sqlite fallback
```

## CLI with Redis

```bash
# Redis URL passed via code (env var not yet supported in CLI)
agent-memory init --storage redis
```

## Architecture

- Local `memories` list maintained for search/scan operations
- Redis used as primary storage for TTL persistence
- `_save_redis()` / `_load_redis()` methods handle sync
- `ttl_remaining()` queries Redis `TTL` directly

## Dependencies

```bash
pip install redis>=4.0
```

---
*Implemented by AI SaaS Lab - 2026-03-21*
