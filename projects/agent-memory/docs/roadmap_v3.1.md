# Agent Memory v3.1 Roadmap

## Timeline: Q1 2026 ✅ Released 2026-03-21

## Goals
Build the most lightweight, flexible memory library for AI agents

## v3.1.0 - Delivered Features

### ✅ String TTL Support
```python
m = Memory(ttl="7d")  # Auto-expire after 7 days
m.add("session data", ttl="1h")  # "7d", "1h", "30m", "2w", "30s"
```

### ✅ Encryption Backend
```python
m = Memory(encryption_key="password")
m.add("api_key", encrypt=True)  # Fernet AES, PBKDF2HMAC key derivation
```

### ✅ Redis Backend
```python
m = Memory(storage="redis", redis_url="redis://localhost:6379", ttl="30m")
```

### ✅ LangChain Adapter
```python
from agent_memory import LangChainMemory
memory = LangChainMemory(storage="sqlite", path="./memory.db", ttl="7d")
```

## v3.2 - Planned Features

- [ ] PostgreSQL backend
- [ ] MongoDB backend
- [ ] Batch TTL operations
- [ ] Memory compression/summarization

## Priority Matrix
| Feature | Pain | Frequency | Differentiation |
|---------|------|-----------|-----------------|
| TTL | 9 | 9 | 10 |
| Encryption | 8 | 7 | 9 |
| Redis | 7 | 8 | 8 |

## Success Metrics
- [ ] 100+ GitHub stars
- [ ] 500+ PyPI downloads/month
- [ ] 10+ contributing developers

---
*Created by AI SaaS Lab - 2026-03-20 | Updated 2026-03-21*
