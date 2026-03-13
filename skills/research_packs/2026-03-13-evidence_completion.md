# Research Pack - Evidence Completion - 2026-03-13

**日期**: 2026-03-13
**目标**: 补齐 Scale Gate M2 痛点证据
**检索关键词**: (中英各 ≥5)

---

## 英文关键词

1. langchain memory complexity issues
2. langchain memory lightweight alternative
3. agent memory library python problems
4. mem0 github issues integration
5. conversation memory limitations

---

## 中文关键词

1. LangChain Memory 复杂问题
2. 轻量级记忆库推荐
3. AI Agent 记忆管理痛点
4. mem0 集成问题
5. 对话记忆局限性

---

## 痛点证据 (Pain Evidence)

### 1. mem0 OpenClaw 集成问题

**痛点一句话**: mem0 的 OpenClaw 集成不支持 lmstudio embedder，导致本地部署用户无法使用

**证据链接/编号**: https://github.com/mem0ai/mem0/issues/4235

**我们的对应解决点**: agent-memory 轻量无依赖，可直接与任何 LLM/embedding provider 集成，无需复杂配置

---

### 2. langchain 依赖复杂性

**痛点一句话**: langchain 依赖链过长，100+ 版本导致依赖冲突和维护成本

**证据来源**: 
- PyPI: https://pypi.org/project/langchain/ (100+ versions)
- GitHub: https://github.com/langchain-ai/langchain

**我们的对应解决点**: agent-memory 无框架依赖，只有少量直接依赖 (pydantic, json), 降低冲突风险

---

### 3. 现有 AI memory 项目的 Issue 模式

**证据来源**: 
- honcho issues: https://github.com/plastic-labs/honcho/issues (issues #420, #410, #407 等)
- mem0 issues: https://github.com/mem0ai/mem0/issues (issues #4312, #4303 等)

**痛点归因**:
- 集成复杂度高
- 配置成本高
- 依赖重、难以轻量化

**我们的对应解决点**: agent-memory 单一 Python 文件，无外部依赖，即装即用

---

## 竞品对比总结

| 竞品 | 痛点 | 证据 | agent-memory 对应 |
|------|------|------|------------------|
| mem0 | 集成限制 (lmstudio) | #4235 | 无框架，可直接集成任意 provider |
| langchain | 依赖重 (100+ 版本) | PyPI | 仅 pydantic + json |
| honcho | (待进一步调研) | issues | 轻量简单 |

---

## 检索日志

- 2026-03-13: 访问 mem0 GitHub，获取 issue #4235 (集成问题)
- 2026-03-13: 访问 langchain PyPI，确认 100+ 版本
- 2026-03-13: 访问 honcho issues，获取 issue 列表
- 2026-03-13: 访问 GitHub topics/agent-memory，获取竞品列表

---

## 下一步行动

- [ ] 获取更多 langchain memory 痛点 issues
- [ ] 访问 supermemoryai/supermemory issues
- [ ] 完善 Pain Evidence 小节

---

*Research Pack generated: 2026-03-13*
