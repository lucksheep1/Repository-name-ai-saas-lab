# Experiment Log

## 2026-03-06 - MVP Build

### Attempt 1: ReMe-style complex system
**Idea:** Full-featured memory with graph, vectors, etc.
**Problem:** Too complex, 500+ lines, loses "lightweight" promise
**Solution:** Pivot to simple TF-IDF based approach

### Attempt 2: Pure vector DB (FAISS)
**Problem:** Requires extra dependency, harder to install
**Solution:** Use sklearn TF-IDF as default, FAISS as optional backend

### Final: Simple Python library
**Approach:**
- TF-IDF for similarity (sklearn)
- JSON for persistence
- Simple API: add, search, get_context

**Result:** ~150 lines, minimal dependencies, works out of box

### Next Steps
- [ ] Test with real agent
- [ ] Add FAISS backend
- [ ] Add LLM summary

---

## 2026-03-21 - v3.1 Feature Release

### Attempt: String TTL + Encryption + Redis Backend

**What worked:**
- `parse_ttl()` — human-readable TTL string parsing ("7d", "1h", "30m", "2w", "30s")
- PBKDF2HMAC key derivation for encryption (Fernet AES)
- Redis backend with native SETEX TTL, graceful fallback
- Sentinel value to distinguish `ttl=None` vs unset

**Problems encountered:**
- Fernet requires 32-byte URL-safe base64 key — had to add PBKDF2HMAC derivation
- PBKDF2 import was wrong name (was `PBKDF2`, correct is `PBKDF2HMAC`)
- Redis `setex` needs `None` handled for TTL=0 case
- `clear()` didn't clear Redis keys — fixed with `delete(*keys)`

**Result:** v3.1 complete — String TTL, Encryption, Redis Backend all working
