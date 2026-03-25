# ⚡ Agent Memory - 3 Lines to Remember Anything

[![CI](https://github.com/lucksheep1/Repository-name-ai-saas-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/lucksheep1/Repository-name-ai-saas-lab/actions)
[![Live Demo](https://img.shields.io/badge/Live-Demo-blue)](https://lucksheep1.github.io/Repository-name-ai-saas-lab/)
[![PyPI Version](https://img.shields.io/pypi/v/agent-memory)](https://pypi.org/project/agent-memory/)

```python
from agent_memory import Memory
m = Memory(storage="json")
m.add("User likes dark mode")
```

> 📢 **[Give Feedback →](https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues)** | 📦 **[v3.1 Release](docs/releases/v3.1.md)**

---

Lightweight memory for AI agents. No LangChain bloat. **v3.1: String TTL + Encryption + Redis!**

## Problem

Agents need to remember context across conversations, but existing solutions are either:
- Too complex (ReMe, langchain.memory)
- Too coupled (framework-specific)
- Too heavy (many dependencies)
- No persistent storage

## Solution

A simple, standalone Python library for agent memory:
- **Lightweight**: ~200 lines, minimal dependencies
- **Flexible**: Multiple storage backends (JSON, FAISS, SQLite)
- **TTL Support**: String format ("7d", "1h", "30m", "2w") — automatic memory decay
- **Encryption**: Optional Fernet encryption for sensitive data
- **Redis Backend**: Distributed memory for multi-agent systems
- **Auto-summary**: Compresses old memories
- **Easy integration**: Any Python project

## Installation

```bash
pip install agent-memory

# For SQLite support (included in standard library)
# No extra dependencies needed!

# For FAISS support (optional)
pip install faiss-cpu

# For Redis backend (optional)
pip install redis

# For encryption (optional)
pip install cryptography
```

## Usage

```python
from agent_memory import Memory

# Initialize memory with SQLite (recommended for production)
memory = Memory(storage="sqlite", path="./memory.db", ttl="7d")

# Add a memory with string TTL (auto-expires in 1 hour)
memory.add("User prefers dark mode", ttl="1h")

# Add with encryption (sensitive data)
memory.add("api_key_xxx", encrypt=True)

# Add with Redis backend (multi-agent)
memory = Memory(storage="redis", redis_url="redis://localhost:6379", ttl="30m")

# Add with tags
memory.add_with_tags("Bug in login", tags=["bug", "urgent"])

# Add with priority
memory.add("Important task", metadata={"priority": 5})

# Search memories
results = memory.search("theme preferences")
print(results)

# Get by tag
bug_memories = memory.get_by_tag("bug")

# Get by priority
important = memory.get_by_priority(4)

# Get context for agent
context = memory.get_context(max_tokens=2000)

# Get timeline
timeline = memory.get_timeline()

# Export to JSON
memory.export("backup.json")

# Export to Markdown
memory.export_markdown("memory.md")
```

## CLI

```bash
# Initialize memory
agent-memory init

# Add a memory (TTL: 7d, 1h, 30m, etc.)
AGENT_MEMORY_TTL=7d agent-memory add "User prefers dark mode"

# Add encrypted memory
AGENT_MEMORY_KEY=mykey agent-memory add "api_key_xxx" --encrypt

# Search memories
agent-memory search "preferences"

# List all memories
agent-memory list

# Show statistics
agent-memory stats

# Delete a memory
agent-memory delete <memory_id>

# Clear all memories
agent-memory clear
```

Environment variables:
- `AGENT_MEMORY_PATH` — path to memory file (default: ./memory.json)
- `AGENT_MEMORY_TTL` — default TTL for all memories (e.g., "7d")
- `AGENT_MEMORY_KEY` — encryption key for sensitive data

# Export to Markdown
agent-memory export --file memory.md --format markdown

# Import
agent-memory import --file backup.json

# Get timeline
agent-memory timeline --top-k 20
```

## Storage Backends

- `json` - Simple JSON file (default, for development)
- `sqlite` - SQLite database (recommended for production, supports TTL)
- `faiss` - FAISS vector store (if available, for similarity search)

### TTL (Time-To-Live)

SQLite backend supports automatic memory expiration:
```python
# Default TTL for all memories
memory = Memory(storage="sqlite", path="./memory.db", ttl_days=30)

# Per-memory TTL
memory.add("Temporary note", ttl_days=7)
```

## API

### Memory.add(text: str, metadata: dict = None, ttl_days: int = None) -> str
Add a new memory. Optionally set TTL (days until expiration).

### Memory.add_with_tags(text: str, tags: List[str], metadata: dict = None) -> str
Add a memory with tags.

### Memory.search(query: str, top_k: int = 5) -> List[Dict]
Search memories by similarity.

### Memory.get_by_tag(tag: str) -> List[Dict]
Get memories by tag.

### Memory.get_by_priority(min_priority: int = 3) -> List[Dict]
Get memories by minimum priority.

### Memory.get_context(max_tokens: int = 2000, max_memories: int = 10) -> str
Get condensed context for agent.

### Memory.get_timeline(limit: int = 20) -> List[Dict]
Get memories as timeline.

### Memory.get_recent(limit: int = 10) -> List[Dict]
Get recent memories.

### Memory.summarize() -> str
Generate a summary of all memories.

### Memory.export(filepath: str)
Export to JSON file.

### Memory.export_markdown(filepath: str)
Export to Markdown file.

### Memory.import_(filepath: str)
Import from JSON file.

### Memory.delete(memory_id: str) -> bool
Delete a memory by ID.

### Memory.clear()
Clear all memories.

### Memory.count() -> int
Get number of memories.

## Limits

- Simple embedding (TF-IDF based)
- No LLM summary yet (coming soon)

## v3.0 Features (2026-03-17)

- ✅ SQLite backend (production-ready persistence)
- ✅ TTL support (automatic memory expiration)
- ✅ Tags and priority system
- ✅ JSON and FAISS backends
- ✅ Markdown export

## Next

- [ ] Add LLM-based summary
- [ ] Add more embedding options
- [ ] Add knowledge graph support

---
*Built: 2026-03-06*
*Updated: 2026-03-17 - v3.0 Release*

## Feedback

🐛 [Report Bug](https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues)
💡 [Request Feature](https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues)
