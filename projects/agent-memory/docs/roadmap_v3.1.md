# Agent Memory v3.1 Roadmap

## Timeline: Q2 2026

## Goals
Build the most lightweight, flexible memory library for AI agents

## Planned Features

### 1. TTL Support (Time-To-Live)
```python
m = Memory(ttl="7d")  # Auto-expire after 7 days
m.add("session data", ttl="1h")
```

### 2. Encryption Backend
```python
m = Memory(storage="encrypted", key=os.environ["MEMORY_KEY"])
m.add("api_key", encrypt=True)
```

### 3. New Storage Backends
- [ ] Redis (high demand)
- [ ] PostgreSQL 
- [ ] MongoDB

### 4. Performance Improvements
- Lazy loading
- Batch operations
- Connection pooling

## Priority Matrix
| Feature | Pain | Frequency | Differentiation |
|---------|------|-----------|-----------------|
| TTL | 9 | 9 | 10 |
| Encryption | 8 | 7 | 9 |
| Redis | 7 | 8 | 8 |

## Success Metrics
- 100+ GitHub stars
- 500+ PyPI downloads/month
- 10+ contributing developers

---
*Roadmap created by AI SaaS Lab - 2026-03-20*
