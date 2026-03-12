# Competition Analysis Playbook

## 目标
竞品对比分析，产出合规 Evidence，支撑差异化定位

---

## Evidence 合规要求

只接受三类 Evidence：
1. 竞品/替代方案主页 (PyPI/NPM/GitHub repo)
2. 竞品 issue/discussion/PR (链接或编号)
3. 官方文档/规范 (链接)

**禁止**:
- 我们自己的仓库链接
- 主观推断 (需 issue/discussion 佐证)

---

## 竞品分析步骤

### 1. 确定竞品范围
- 直接竞品 (功能相似)
- 间接竞品 (解决相似问题)
- 替代方案 (开源/商业)

### 2. 收集 Evidence

#### 竞品主页 ( Existence)
```bash
# PyPI 搜索
curl https://pypi.org/pypi/<package>/json

# GitHub 搜索
https://github.com/search?q=<keyword>+<use-case>
```

#### 痛点证据 ( Pain Points)
- GitHub Issues: "problem", "bug", "complex", "heavy"
- GitHub Discussions: "alternative", "better", "simpler"
- PR/Commit: 修复的问题

#### 文档/复杂性
- 官方文档长度
- 依赖数量
- 配置复杂度

### 3. 产出对比表

| 竞品 | 痛点 | Evidence |
|------|------|----------|
| langchain.memory | 依赖框架，重 | https://pypi.org/project/langchain/ |

---

## 验证方式

```bash
# 验证竞品链接
curl -I <竞品链接>

# 检查竞品 issue
https://github.com/<org>/<repo>/issues?q=<keyword>
```

---

## 成功标准

- 每个关键问题 ≥3 条合规 Evidence
- 差异化结论有证据支撑
- 无效 Evidence 已迁移到非 Evidence section
