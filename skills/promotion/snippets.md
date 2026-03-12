# Promotion Snippets

## Show HN 投稿模板

```markdown
Show HN: 轻量级 Agent 记忆管理库 (Python)

项目: agent-memory
GitHub: https://github.com/lucksheep1/Repository-name-ai-saas-lab

解决的问题:
- 现有方案太重 (langchain.memory)
- 需要简单的上下文记忆

特点:
- 单一文件，无框架依赖
- 150 行代码
- 支持标签、优先级、搜索

安装: pip install agent-memory
演示: (Quick Demo 输出)
```

---

## Twitter 推广文案

```text
🚀 Just released agent-memory v1.0.0

Lightweight memory management for AI agents

✅ Single file (~150 lines)
✅ No framework dependency
✅ Tags, priority, search

pip install agent-memory

#AI #DevTools #OpenSource #Python
```

---

## Reddit 发帖模板

```markdown
## Project: agent-memory

I built a lightweight memory manager for AI agents because existing solutions (langchain.memory, etc.) are too heavy for my use case.

### Features
- Simple API (add, search, get_context)
- Tagging and priority support
- JSON/FAISS storage backends
- CLI tool included

### Quick Demo
```python
from agent_memory import Memory
memory = Memory()
memory.add("User prefers dark mode")
memory.search("theme")
```

### Why lighter?
- Single file, no framework
- Minimal dependencies
- Easy to understand/modify

GitHub: [link]
PyPI: [link]

Feedback welcome!
```

---

## README Quick Demo 模板

```markdown
## Quick Start

```bash
pip install agent-memory
```

```python
from agent_memory import Memory

# Initialize
memory = Memory(storage="json", path="./memory.json")

# Add memories
memory.add("User prefers dark mode")
memory.add_with_tags("Bug in login", tags=["bug", "urgent"])

# Search
results = memory.search("theme")
print(results)

# Get context for LLM
context = memory.get_context(max_tokens=2000)
print(context)
```

Expected output:
[显示预期输出]
```
