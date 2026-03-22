# Feature: TTL + Encryption Support

## Status: ✅ Implemented in v3.1.0

## String TTL Format

```python
from agent_memory import Memory, parse_ttl

# Global TTL (all memories)
m = Memory(ttl="7d")

# Per-memory TTL
m.add("session data", ttl="1h")    # 1 hour
m.add("temp cache", ttl="30m")    # 30 minutes
m.add("weekly task", ttl="2w")     # 2 weeks
m.add("debug trace", ttl="30s")     # 30 seconds

# Check remaining TTL
rem = m.ttl_remaining(memory_id)
print(f"Expires in {rem:.0f}s")
```

**Supported formats:** `Ns` (seconds), `Nm` (minutes), `Nh` (hours), `Nd` (days), `Nw` (weeks)

## Encryption

```python
from agent_memory import Memory

# Initialize with encryption
m = Memory(encryption_key="your-password")

# Add encrypted memory
m.add("sk-api-key-12345", encrypt=True)

# Automatic decryption on retrieval
data = m.get(memory_id)
print(data["text"])  # Decrypted automatically
```

Key derivation: Password → PBKDF2-HMAC-SHA256 → 32-byte Fernet key.

## Redis Backend with TTL

```python
from agent_memory import Memory

m = Memory(
    storage="redis",
    redis_url="redis://localhost:6379",
    ttl="30m"
)

# Memories automatically expire in Redis
m.add("temp session data", ttl="1h")
```

## Migration from v3.0

```python
# v3.0
m = Memory(ttl_days=7)
m.add("data", ttl_days=1)

# v3.1 (backward compatible)
m = Memory(ttl="7d")
m.add("data", ttl="1h")
m.add("data", ttl=1)        # still works (days as int)
m.add("data", ttl=None)     # explicitly no TTL
```

---
*Implemented by AI SaaS Lab - 2026-03-21*
