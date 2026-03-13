# Outreach Pack #1: LangChain Users

**Target Channel**: LangChain GitHub Discussions / Issues
**Pack Version**: 1.0
**Created**: 2026-03-13

---

## 目标人群
- LangChain 用户正在寻找更简单的 memory 解决方案
- 已被 LangChain complexity 困扰的开发者

## 标题

"被 LangChain memory 复杂度困扰？试试轻量替代方案"

## 正文

```
我正在开发 agent-memory (https://github.com/lucksheep1/Repository-name-ai-saas-lab)，一个 ~150 行的轻量级 agent 记忆库。

背景：看到你在 LangChain discussions 中提到 memory 模块复杂，想问一下：
- 你最困扰的点是什么？
- 如果有一个更轻量的方案，会考虑迁移吗？

Quick Demo：
pip install agent-memory
from agent_memory import Memory
memory.add("user preference")
context = memory.get_context(max_tokens=2000)

期待你的反馈！
```

## 3 个引导问题

1. 你现在用 LangChain memory 最大的痛点是什么？
2. 如果 agent-memory 支持 LangChain 集成，你会试用吗？
3. 你愿意为什么功能付费？

## 链接

- Quick Demo: docs/site/index.html
- Landing: docs/site/index.html
- Feedback Pack: docs/feedback/packs/2026-03-13.md

## 成功标准

- 获得 ≥1 条实质性回复
- 获得 ≥1 个 Issue/Feature Request

---
