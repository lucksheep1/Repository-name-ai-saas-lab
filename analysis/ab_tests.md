# A/B Tests - Copy Learning

**Generated**: 2026-03-13
**Project**: agent-memory

---

## 当前版本

### README 开头 (当前)

```
# Agent Memory Manager

> **🎯 Feedback Wanted!** [Share your feedback →](../../docs/feedback/packs/2026-03-13.md)  
> **📖 Landing Page:** [docs/site/index.html](../../docs/site/index.html) *(clone repo to view)*  
> **📦 Release:** [v1.0.0](../../docs/releases/v1.0.0.md)  
> **💬 Discuss:** [GitHub Discussions](https://github.com/lucksheep1/Repository-name-ai-saas-lab/discussions)

Lightweight memory management for AI agents.

## Problem

Agents need to remember context across conversations, but existing solutions are either:
- Too complex (ReMe, langchain.memory)
- Too coupled (framework-specific)
- Too heavy (many dependencies)
```

---

## A/B 版本

### Version A: 轻量依赖 / 分钟上手

**定位**: 强调易用性、上手速度

**README 开头**:

```
# Agent Memory Manager

> 5 minutes to integrate. No LangChain required.

Lightweight memory management for AI agents.

## Quick Start

pip install agent-memory

```python
from agent_memory import Memory
memory = Memory(storage="json", path="./memory.json")
memory.add("User prefers dark mode")
context = memory.get_context(max_tokens=2000)
```

## Why?

- 150 lines of code
- 2 dependencies only
- Works with or without LangChain
```

### Version B: 对比痛点 / Evidence 驱动

**定位**: 引用 pain evidence，强调差异化

**README 开头**:

```
# Agent Memory Manager

> Built because LangChain's memory is too complex.

Lightweight memory management for AI agents.

## The Problem

From GitHub issues and discussions, we found:
- LangChain has 100+ packages (PyPI)
- Memory module requires framework knowledge
- Users want "simpler alternatives"

## Solution

agent-memory: ~150 lines, minimal dependencies

```python
from agent_memory import Memory
memory = Memory(storage="json", path="./memory.json")
memory.add("User prefers dark mode")
context = memory.get_context(max_tokens=2000)
```
```

---

## 版本对比

| 维度 | Version A | Version B |
|------|-----------|-----------|
| 主打 | 轻量 / 易上手 | 解决痛点 / 证据驱动 |
| 用户心理 | "试试看" | "解决我问题" |
| Evidence | 无 | 有 (100+ packages) |
| 适用场景 | Maker / 学生 | 开发者 / 企业 |

---

## 为什么这样写 (证据/预期)

### Version A
- **假设**: 轻量是最大卖点，用户想快速试用
- **证据**: Hackathon、社区反馈强调"5 分钟上手"
- **预期**: 高转化试用

### Version B
- **假设**: 开发者关心"为什么做"，需要差异化理由
- **证据**: langchain issues 提及 complexity, mem0 issues 提及集成问题
- **预期**: 高质量用户

---

## 下一轮改进计划

### 从 Version A 学到
- 突出 "5 minutes" 量化指标
- 去掉复杂描述

### 从 Version B 学到
- 添加更多 pain evidence 链接
- 区分"简单"和"简陋"

### 建议改进
1. 合并两版优点：A 的简洁 + B 的证据
2. 添加量化对比表
3. 考虑目标人群切换版本

---

## Landing Page A/B

### Version A: https://agentmemory.example (轻量)

```html
<h1>⚡ agent-memory</h1>
<p>Lightweight memory for AI agents.</p>
<p>5 minutes to integrate.</p>
```

### Version B: 对比痛点

```html
<h1>⚡ agent-memory</h1>
<p>150 lines vs LangChain's 100+ packages.</p>
<p>Because simplicity matters.</p>
```

---

## 后续测试

- 监控 Click-through rate
- 收集用户反馈偏好
- 迭代版本

---
