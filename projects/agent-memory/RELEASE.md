# Release Notes - v1.0.0

**Version**: 1.0.0
**Date**: 2026-03-13
**Project**: agent-memory

---

## Quick Demo

```python
pip install agent-memory
```

```python
from agent_memory import Memory

memory = Memory(storage="json", path="./memory.json")
memory.add("User prefers dark mode")
memory.add("User's name is Alice")
context = memory.get_context(max_tokens=2000)
print(context)
```

---

## What's New (v1.0.0)

### Core Features
- ✅ Memory storage (JSON/SQLite)
- ✅ Search functionality
- ✅ Tag management
- ✅ Priority system
- ✅ Timeline view
- ✅ Export/Import (JSON/Markdown)
- ✅ LangChain integration example

### Examples
- `quickstart.py` - Basic usage
- `langchain_example.py` - LangChain integration
- `multi_agent_example.py` - Multi-agent sharing
- `api_server.py` - FastAPI server
- `integration_demo.py` - Complete workflow demo

### Feedback
- Issue templates (Bug/Feature)
- Discussion board
- Feedback packs
- Landing page

---

## Links

| Resource | Link |
|----------|------|
| GitHub | https://github.com/lucksheep1/Repository-name-ai-saas-lab |
| Landing | docs/site/index.html (clone to view) |
| Feedback | https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues |
| Discussions | https://github.com/lucksheep1/Repository-name-ai-saas-lab/discussions |

---

## Changelog

### v1.0.0 (2026-03-13)
- Initial release
- Core memory management
- Multiple storage backends
- Tag & priority system
- Timeline view
- LangChain integration
- FastAPI server example

---

*Release v1.0.0 - 2026-03-13*
