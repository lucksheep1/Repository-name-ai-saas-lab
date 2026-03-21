# Release Notes - v3.1.0

**Version**: 3.1.0
**Date**: 2026-03-21
**Project**: agent-memory

---

## Install

```bash
pip install agent-memory
```

---

## What's New in v3.1

### ✨ Human-Readable String TTL

```python
from agent_memory import Memory

m = Memory(ttl="7d")
m.add("session data", ttl="1h")  # "7d", "1h", "30m", "2w", "30s"
```

### 🔒 Encryption Support

```python
m = Memory(encryption_key="my-password")
m.add("api_key_xxx", encrypt=True)  # Auto-encrypts, auto-decrypts on get()
```

### 🗄️ Redis Backend

```python
m = Memory(storage="redis", redis_url="redis://localhost:6379", ttl="30m")
```

### CLI

```bash
agent-memory init
AGENT_MEMORY_TTL=7d agent-memory add "User prefers dark mode"
AGENT_MEMORY_KEY=mykey agent-memory add "secret" --encrypt
agent-memory search "preferences"
agent-memory stats
```

---

## Full Changelog

### v3.1.0 (2026-03-21)
- String TTL format: "7d", "1h", "30m", "2w", "30s"
- Fernet AES encryption (PBKDF2HMAC key derivation)
- Redis backend with native SETEX TTL
- `Memory.ttl_remaining()` query method
- `Memory.get()` with auto-decryption
- Sentinel value fix for `ttl=None` vs unset
- Full CLI tool: init/add/search/list/delete/clear/stats
- `test_all_backends.py` verification script

### v1.0.0 (2026-03-13)
- Initial release
- JSON/SQLite storage
- TF-IDF search
- Tag & priority system
- Timeline view
- Export/Import
- LangChain integration

---

## Links

| Resource | Link |
|----------|------|
| GitHub | https://github.com/lucksheep1/Repository-name-ai-saas-lab |
| Detailed Release | docs/releases/v3.1.md |
| Feedback | https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues |

---

*Release v3.1.0 - 2026-03-21*
