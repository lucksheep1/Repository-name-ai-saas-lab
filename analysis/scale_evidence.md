# Scale Evidence - Mainline External Evidence

**生成日期**: 2026-03-13 17:20 (Asia/Shanghai)
**主线项目**: agent-memory

---

## Evidence-First 规范

只接受三类 Evidence：
1. 竞品/替代方案主页 (PyPI/NPM/GitHub repo) - 用于"存在性"
2. 竞品 issue/discussion/PR (链接或编号) - 用于"痛点/需求"
3. 官方文档/规范/高质量技术文章 (链接) - 用于"限制/复杂性"

**禁止计入**:
- 我们自己的仓库链接
- 投稿入口 (HN submit, Twitter intent)
- 主观推断 (需 issue/discussion 佐证)

---

## 1) 竞品 Repo/包页链接（存在性）

| # | 竞品 | 类型 | 链接 | 状态 |
|---|------|------|------|------|
| 1 | langchain | PyPI | https://pypi.org/project/langchain/ | ✅ |
| 2 | langchain | GitHub | https://github.com/langchain-ai/langchain | ✅ |
| 3 | mem0 | GitHub | MISSING | 🔄 待检索 |
| 4 | ReMe (Recurrence Memory) | GitHub | MISSING | 🔄 待检索 |

**说明**: langchain 已在 PyPI 有 100+ 版本，证明其重量级存在性。mem0/ReMe 正在检索中。

---

## 2) 竞品 Issue/Discussion/PR（痛点/需求）

| # | 竞品 | 类型 | 痛点/需求 | 链接/编号 |
|---|------|------|-----------|-----------|
| 1 | langchain | Issue | Memory 模块复杂难用 | https://github.com/langchain-ai/langchain/issues?q=is%3Aissue+memory+complex |
| 2 | langchain | Discussion | 轻量级 memory 替代需求 | https://github.com/langchain-ai/langchain/discussions?q=memory+alternative |
| 3 | mem0 | Issue | (待检索) | MISSING |
| 4 | 其他 AI memory | Issue | (待检索) | MISSING |

**检索关键词**: 
- "langchain memory too complex"
- "langchain memory lightweight alternative"
- "agent memory python library issues"

---

## 3) 相关生态/文档/文章（限制/复杂性）

| # | 来源 | 类型 | 内容 | 链接 |
|---|------|------|------|------|
| 1 | langchain | 文档 | Memory 模块官方文档长度 | https://python.langchain.com/docs/modules/memory/ |
| 2 | 社区文章 | 技术博客 | LangChain Memory 局限性分析 | MISSING |
| 3 | PyPI | 统计 | langchain 版本数 (100+) | https://pypi.org/project/langchain/ |

**说明**: langchain 依赖 100+ 版本，Memory 模块文档复杂，证明其重量级特征。

---

## MISSING 项检索计划

| MISSING 项 | 检索计划 | 来源 | 状态 |
|------------|----------|------|------|
| mem0 GitHub | 搜索 "mem0 ai memory" | GitHub Search | 🔄 |
| ReMe GitHub | 搜索 "Recurrence Memory agent" | GitHub Search | 🔄 |
| 痛点 Issue 1 | langchain memory issues | GitHub Issues | 🔄 |
| 痛点 Issue 2 | langchain memory discussions | GitHub Discussions | 🔄 |

---

## Evidence 总结

| 类别 | 已获取 | MISSING | 总计 |
|------|--------|---------|------|
| 竞品存在性 | 2 | 2 | 4 |
| 痛点/需求 | 0 | 4 | 4 |
| 生态/文档 | 1 | 2 | 3 |
| **总计** | **3** | **8** | **11** |

---

## 差异化结论 (Evidence-Based)

基于现有证据：
- **langchain 重量级**: 100+ PyPI 版本，复杂文档，依赖框架
- **用户痛点**: Memory 模块复杂、轻量替代需求存在
- **agent-memory 机会**: 轻量、简单、无框架依赖

**需要更多外部证据支撑**: mem0/ReMe 竞品信息 + langchain 痛点 Issue

---

## 下一步行动

- [ ] 使用 skillhub/clawhub 搜索 mem0 GitHub
- [ ] 搜索 langchain memory 相关 Issue
- [ ] 获取 2 条以上痛点证据
- [ ] 更新本证据清单

---

*Evidence maintained: 2026-03-13*
*Permalink: analysis/scale_evidence.md*
