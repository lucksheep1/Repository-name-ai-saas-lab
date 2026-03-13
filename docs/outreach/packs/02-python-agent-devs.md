# Outreach Pack #2: Python Agent Developers

**Target Channel**: Python AI/ML Discord / Reddit r/MachineLearning
**Pack Version**: 1.0
**Created**: 2026-03-13

---

## 目标人群
- 构建 AI agents 的 Python 开发者
- 需要管理对话上下文的开发者

## 标题

"你的 agent 还在丢失上下文？试试这个 150 行的解决方案"

## 正文

```
分享一个我正在开发的小工具：agent-memory

背景：我的 agent 总是丢失对话上下文，试了 LangChain、mem0 都太重了。

我的方案：
- 150 行代码，无框架依赖
- JSON/SQLite 存储
- 支持 tag、优先级、时间线

from agent_memory import Memory
memory = Memory(storage="json", path="./memory.json")
memory.add("User prefers dark mode")
context = memory.get_context(max_tokens=2000)

有兴趣的兄弟欢迎反馈！
```

## 3 个引导问题

1. 你现在怎么处理 agent 上下文丢失问题？
2. 最看重 memory 库的哪个功能？
3. 有什么可以改进的地方？

## 链接

- Quick Demo: docs/site/index.html
- Landing: docs/site/index.html
- Feedback Pack: docs/feedback/packs/2026-03-13.md

## 成功标准

- 获得 ≥1 条实质性回复
- Reddit post 获得 ≥10 upvotes

---
