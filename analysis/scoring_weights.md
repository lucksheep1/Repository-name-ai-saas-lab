# Scoring Weights

## Evidence 权重表 (Evidence-First 规范)

| 证据类型 | 权重 | 计入 Evidence? | 说明 |
|----------|------|---------------|------|
| **Issue/Discussion/PR** | **最高 (3.0)** | ✅ | 直接反映用户痛点需求 |
| **官方文档/规范** | **中等 (2.0)** | ✅ | 反映限制/复杂性 |
| **竞品主页 (PyPI/NPM)** | **中等 (2.0)** | ✅ | 证明存在性 |
| **Stars/Trending** | **低 (1.0)** | ❌ | 只能用于方向发现，不能作为痛点证据 |
| **本地可运行验证** | **不计入** | ❌ | 只计入 Verification，不计入 Evidence |

### Evidence 语义规则

**只允许计入**:
1. 竞品/替代方案主页 (PyPI/NPM/GitHub repo) - 用于"存在性"
2. 竞品 issue/discussion/PR (链接或编号) - 用于"痛点/需求"
3. 官方文档/规范/高质量技术文章 (链接) - 用于"限制/复杂性"

**禁止计入**:
- 我们自己的仓库链接
- 投稿入口 (HN submit, Twitter intent)
- 主观推断 (需 issue/discussion 佐证)

## 证据类型权重

| 证据类型 | 权重 | 说明 |
|----------|------|------|
| GitHub Issue | 3.0 | 真实用户痛点 |
| GitHub Discussion | 2.5 | 社区讨论 |
| GitHub Review | 2.0 | 代码审查中的需求 |
| Hacker News | 2.0 | 社区关注度 |
| Product Hunt | 1.5 | 产品验证 |
| Reddit | 1.5 | 社区讨论 |
| 博客/文章 | 1.0 | 二手信息 |

## 扫描来源优先级

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | GitHub Issues | 最高价值 |
| 2 | GitHub Trending | 趋势信号 |
| 3 | Hacker News | 社区讨论 |
| 4 | GitHub Discussions | 次高价值 |

## 项目评分标准

| 维度 | 权重 | 阈值 |
|------|------|------|
| Pain | 2.0 | ≥7 进入开发 |
| Frequency | 1.5 | ≥6 |
| Ease | 1.0 | ≥7 |
| Market | 1.5 | ≥6 |

## 决策规则

- **Promising**: ≥3 条证据 + 可运行验证
- **Iterate**: ≥2 条证据 + MVP 完成
- **Kill**: 证据 <2 条

---
*Generated: 2026-03-06*
