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
