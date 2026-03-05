# Opportunity Report — 2026-03-05

## Opportunity 1: Claude Code Skill Templates

**Problem Summary:**
开发者需要大量重复创建相似的 skill 文件（如 file ops, git, code review），但缺乏可复用的模板库。

**Evidence (3+):**
1. Agent-Skills-for-Context-Engineering (13k stars/week) - 证明 skill 模板需求旺盛
2. obra/superpowers (71k stars) - 方法论 + skills 框架需求强烈
3. GitHub 多个 MCP 相关项目 trending

**Existing Solutions:**
- anthropics/skill: 官方示例，数量有限
- 社区分散的各色 skill 库

**Why They Fail:**
- 分散在各处，无统一格式
- 缺乏可发现性
- 无标准化测试/验证

**Possible MVP (1-4h):**
- 创建 5-10 个最常用的 skill 模板
- 统一格式 + README + 验证脚本

**Opportunity Score:**
- Pain: 7/10
- Frequency: 8/10
- Ease: 9/10 (纯文本+脚本)
- Market: 7/10

---

## Opportunity 2: Local-First Code RAG

**Problem Summary:**
开发者想在本地构建代码知识图谱，但不希望依赖云服务（隐私/速度顾虑）。

**Evidence:**
1. GitNexus (9.8k stars) - 客户端知识图谱需求明显
2. 多个开源 RAG 项目 trending

**Existing Solutions:**
- GitNexus (browser-based)
- Sourcegraph (云优先)
- local-rag 各种散落项目

**Why They Fail:**
- 大多需要云后端
- 缺乏轻量级 CLI 方案

**Possible MVP:**
- 基于 embedding 的本地代码搜索 CLI
- 支持常见编程语言

**Opportunity Score:**
- Pain: 6/10
- Frequency: 7/10
- Ease: 6/10 (需处理代码解析)
- Market: 6/10

---

## Opportunity 3: MCP Server Quick-Start

**Problem Summary:**
MCP (Model Context Protocol) 生态爆发，但开发者不知道如何快速创建自己的 MCP server。

**Evidence:**
1. GitHub 主页出现 "MCP Registry" 入口
2. 多个 MCP 相关项目 trending

**Existing Solutions:**
- 官方文档示例
- mcp-typescript, mcp-python 模板

**Why They Fail:**
- 缺乏中文/中文友好教程
- 示例零散

**Possible MVP:**
- 一键生成 MCP server 的 CLI 工具
- 内置常用工具模板

**Opportunity Score:**
- Pain: 8/10
- Frequency: 9/10
- Ease: 8/10
- Market: 8/10

---

*Scanner Complete: 2026-03-05 21:35 GMT+8*
*Top Pick: Opportunity 3 (MCP Server Quick-Start) - 高频+易实现*
