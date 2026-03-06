# Agent Memory Manager

Lightweight memory management for AI agents.

## Problem

Agents need to remember context across conversations, but existing solutions are either:
- Too complex (ReMe, langchain.memory)
- Too coupled (framework-specific)
- Too heavy (many dependencies)

## Solution

A simple, standalone Python library for agent memory:
- **Lightweight**: ~150 lines, minimal dependencies
- **Flexible**: Multiple storage backends
- **Auto-summary**: Compresses old memories
- **Easy integration**: Any Python project

## Installation

```bash
pip install agent-memory
```

## Usage

```python
from agent_memory import Memory

# Initialize memory
memory = Memory(storage="json", path="./memory.json")

# Add a memory
memory.add("User prefers dark mode")

# Search memories
results = memory.search("theme preferences")
print(results)

# Get context for agent
context = memory.get_context(max_tokens=2000)
```

## Storage Backends

- `json` - Simple JSON file (default)
- `faiss` - FAISS vector store (if available)

## API

### Memory.add(text: str)
Add a new memory.

### Memory.search(query: str, top_k: int = 5) -> List[Dict]
Search memories by similarity.

### Memory.get_context(max_tokens: int = 2000) -> str
Get condensed context for agent.

### Memory.clear()
Clear all memories.

## Limits

- No persistence across restarts (for json backend)
- Simple embedding (TF-IDF based)
- No LLM summary yet (coming soon)

## Next

- [ ] Add FAISS backend
- [ ] Add LLM-based summary
- [ ] Add more embedding options

---
*Built: 2026-03-06*
