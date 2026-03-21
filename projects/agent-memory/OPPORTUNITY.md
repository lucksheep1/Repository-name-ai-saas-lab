# Opportunity & Evidence

## 项目: Agent Memory Manager (v3.1)

### Evidence Quality: 9/10

### 可追溯来源 (5+)

1. **LangChain GitHub Issues (核心证据)**
   - 44 open issues mentioning "memory" in langchain-ai/langchain
   - Issue #34930: "Memory leaks in plain LLM calls" (5 comments)
   - Issue #36126: "HuggingFaceEmbeddings causes excessive device-to-cpu transfers per batch" (Mar 20, 2026)
   - 来源: https://api.github.com/search/issues?q=repo:langchain-ai/langchain+memory

2. **Hacker News - Ask HN (社区验证)**
   - "Anyone using knowledge graphs for LLM agent memory/context management?" — 12 points
   - Key quote: "once agents need to maintain structured knowledge... context becomes less and less interpretable"
   - 来源: https://news.ycombinator.com/item?id=43940654

3. **Phidata (竞争对手市场验证)**
   - "Build AI Agents with memory, knowledge, tools and reasoning" — HN 27 points
   - 来源: https://github.com/phidatahq/phidata

4. **GitHub Topics - Agent 趋势**
   - 3382 repos 提及 "memory+LLM" (2026-03)
   - 来源: https://github.com/topics/agent

5. **PyPI 空白 (竞争优势)**
   - `agent-memory` 包名未注册 (404 Not Found)
   - 无直接轻量级 pip 竞争对手
   - 来源: https://pypi.org/pypi/agent-memory/json

---

## 项目: AI Tool Security Scanner

### Evidence Quality: 9/10

### 可追溯来源 (3+)

1. **Clinejection 事件** (核心证据)
   - GitHub Issue Title 攻击 4000+ 台机器
   - 来源: 安全事件披露 (2026-03)

2. **npm 安全问题**
   - 恶意 postinstall 脚本检测需求
   - 来源: npm 官方安全报告

3. **GitHub Actions 安全**
   - Cache poisoning, 权限过宽问题
   - 来源: 安全研究报告

4. **Cursor / Cline / AI IDE 流行**
   - AI coding tools 安全风险增加
   - 来源: GitHub Trending / Product Hunt
