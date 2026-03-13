# Feedback Wanted - agent-memory

> **Help us build the agent memory tool you actually need.**

---

## One-Line Value

agent-memory: **~150 lines of code** vs LangChain's **100+ packages**.

Because simplicity matters.

---

## Quick Demo (30 seconds)

```python
# Install
pip install agent-memory

# Use
from agent_memory import Memory
memory = Memory(storage="json", path="./memory.json")
memory.add("User prefers dark mode")
context = memory.get_context(max_tokens=2000)
```

**Landing Page**: [docs/site/index.html](../site/index.html)

---

## 3 Questions We Need Your Answer

### 1. What's your biggest pain point with agent memory?

- [ ] Too complex to set up
- [ ] Too many dependencies
- [ ] Can't integrate with my stack
- [ ] Hard to customize
- [ ] Something else: _____

### 2. What's your primary use case?

- [ ] Chatbot memory
- [ ] Agent workflow context
- [ ] Multi-agent sharing
- [ ] User preference storage
- [ ] Other: _____

### 3. Would you pay for?

- [ ] Cloud sync
- [ ] More storage backends (PostgreSQL, Redis)
- [ ] Enterprise support
- [ ] Nothing / Open source is enough

---

## How to Give Feedback

### Option 1: GitHub Issues
- [Bug Report](https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues/new?template=bug_report.md)
- [Feature Request](https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues/new?template=feature_request.md)

### Option 2: GitHub Discussions
- [General Discussion](https://github.com/lucksheep1/Repository-name-ai-saas-lab/discussions)

### Option 3: Quick Feedback Form
- [Feedback Pack](packs/2026-03-13.md)

---

## Why Your Feedback Matters

Every response shapes our roadmap:

| You say... | We do... |
|------------|----------|
| "Too complex" | Simplify API |
| "Need X storage" | Add backend |
| "Can't integrate with Y" | Add integration |

---

## Current Pain Points We're Addressing

Based on community feedback:

1. **LangChain is too heavy** → agent-memory: 150 lines, 2 dependencies
2. **Integration issues** → Simple JSON/SQLite, no framework lock-in
3. **Setup complexity** → 5-minute integration

---

## Contact

- **GitHub**: https://github.com/lucksheep1/Repository-name-ai-saas-lab
- **Discussions**: https://github.com/lucksheep1/Repository-name-ai-saas-lab/discussions

---

*Last updated: 2026-03-13*
