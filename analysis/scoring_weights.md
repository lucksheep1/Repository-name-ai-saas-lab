# Scoring Weights

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
