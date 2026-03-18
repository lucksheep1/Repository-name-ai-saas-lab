#!/bin/bash
# Hacker News Submit Script
# 用于提交产品更新到 HN

# 使用方法:
# 1. 登录 HN 账号
# 2. 访问 https://news.ycombinator.com/submit
# 3. 填写以下内容:

TITLE="Agent Memory v3.0 - SQLite-based Memory for AI Agents"
URL="https://github.com/lucksheep1/ai-saas-lab/tree/main/projects/agent-memory"
TEXT="

## Agent Memory v3.0 Released

A lightweight, SQLite-based memory system for AI agents with TTL support.

### Features
- SQLite persistence
- TTL (Time To Live) support
- LangChain adapter included
- Zero dependencies

### Quick Start
\`\`\`python
from agent_memory import AgentMemory
mem = AgentMemory()
mem.add(\"key\", \"value\")
\`\`\`

### GitHub
https://github.com/lucksheep1/ai-saas-lab/tree/main/projects/agent-memory
"

echo "请手动复制以上内容到 HN Submit 页面"
echo "URL: https://news.ycombinator.com/submit"
