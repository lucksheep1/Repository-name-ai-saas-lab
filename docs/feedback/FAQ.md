# FAQ - agent-memory

## 什么是 agent-memory？
agent-memory 是一个为 AI Agent 设计的持久化记忆管理框架，支持多会话记忆检索和上下文管理。

## 谁应该使用？
- AI 开发者构建需要长期记忆的 Agent
- 需要跨会话上下文保持的自动化系统
- 希望减少上下文窗口浪费的 LLM 应用开发者

## 主要功能
- 持久化记忆存储（SQLite）
- 向量相似度搜索
- 自动记忆摘要
- 多会话上下文管理

## 如何安装？
```bash
pip install agent-memory
```

## 如何使用？
```python
from agent_memory import AgentMemory
memory = AgentMemory()
memory.add("用户喜欢蓝色")
results = memory.search("用户颜色偏好")
```

## 支持哪些 LLM？
- OpenAI GPT 系列
- Anthropic Claude
- 本地模型（兼容 OpenAI API）

## 收费吗？
当前免费，未来考虑团队版订阅。
