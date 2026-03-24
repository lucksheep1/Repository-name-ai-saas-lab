# External Signals - 2026-03-24

Source: Brave Search API (NOT GitHub)

## Key Findings

### 1. LangChain Memory Pain (Reddit)
**URL**: https://www.reddit.com/r/AgentsOfAI/comments/1r8eeb6/are_we_still_using_langchain_in_2026_or_have_you/

> "I don't use LangChain anymore... It's way too heavy... I ended up using SQLite for hard guardrails/safety nets"

**Signal**: 用户明确放弃 LangChain 自己用 SQLite，验证轻量级需求

---

### 2. Serverless Memory Problem (Reddit)
**URL**: https://www.reddit.com/r/LangChain/comments/12z7e63/memory_in_production/

> "All the examples that Langchain gives are for persisting memory locally which won't work in a serverless (stateless) environment"

**Signal**: LangChain memory 不支持 serverless，这是真实痛点

---

### 3. Memory Persistence vs Relevance (Reddit)
**URL**: https://www.reddit.com/r/LangChain/comments/1otz4oi/how_are_you_all_managing_memorycontext_in/

> "The biggest challenge with memory in LangChain agents is balancing persistence with relevance. Storing everything leads to context bloat, too aggressive pruning loses important cues."

**Signal**: 需要智能的 memory 过期/衰减机制

---

### 4. OpenAI Agents SDK (Official)
**URL**: https://openai.github.io/openai-agents-python/

> "lightweight, easy-to-use package with very few abstractions"

**Signal**: OpenAI 官方推轻量级方案，市场趋势确认

---

### 5. Agno Framework
**URL**: https://www.agno.com/agent-framework

> "open-source Python framework for building and running AI agents... ready-made components like memory"

**Signal**: 新框架出现，包含 memory 组件

---

## Conclusion

- **LangChain 太重** 是持续被验证的痛点
- **Serverless memory** 是未解决的场景
- **TTL/智能过期** 是用户真正需要的功能
- 轻量级是市场趋势（OpenAI Agents SDK 也强调 lightweight）

## Next Action

Agent Memory 的差异化：
1. ✅ 轻量（~200 行）
2. ✅ SQLite 后端（serverless 友好）
3. ✅ TTL 过期（解决 context bloat）
4. ✅ 可选的 Redis 分布式

这些功能与外部信号完全匹配。
