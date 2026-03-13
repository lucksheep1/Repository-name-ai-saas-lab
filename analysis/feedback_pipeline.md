# Feedback Pipeline - Collection to Task Conversion

**生成日期**: 2026-03-13 17:25 (Asia/Shanghai)
**目标**: 建立可行动的反馈收集→筛选→转化流程

---

## 1) 反馈入口清单

| 入口 | 路径 | 状态 |
|------|------|------|
| Issue Templates | `docs/feedback/` (Markdown 模板) | ✅ |
| Discussion Starter | `docs/feedback/discussions_stub.md` | 🔄 待创建 |
| Feedback Pack | `docs/feedback/packs/2026-03-13.md` | 🔄 待创建 |
| README Feedback 章节 | `projects/agent-memory/README.md` | ✅ |

---

## 2) 反馈收集 → 筛选 → 转化流程

### 阶段 1: 收集 (Collection)

**入口**:
1. **Issue**: 用户通过 GitHub Issues 提交
2. **Survey**: 用户填写 `docs/feedback/SURVEY.md`
3. **RFC**: 用户使用 `docs/feedback/RFC_TEMPLATE.md` 请求功能

**收集动作**:
- 每日检查新 Issue/Survey/RFC
- 记录到 `docs/feedback/packs/YYYY-MM-DD.md`

### 阶段 2: 筛选 (Triage)

**筛选标准**:

| 维度 | 高优先级 | 中优先级 | 低优先级 |
|------|---------|---------|---------|
| 频率 | 多用户提及 | 1-2 用户 | 偶发 |
| 痛点强度 | 影响核心功能 | 影响体验 | 锦上添花 |
| 实现成本 | <4 小时 | 4-24 小时 | >24 小时 |

**筛选动作**:
1. 去重：合并相似反馈
2. 分类：Bug / Feature / Enhancement / Question
3. 评估：优先级 + 实现成本

### 阶段 3: 转化 (Conversion)

**转化规则**:

| 类型 | 转化目标 | 责任人 |
|------|---------|--------|
| Bug | GitHub Issue (tag: bug) | AI Lab |
| Feature Request | GitHub Issue (tag: enhancement) + RFC | AI Lab |
| Question | FAQ 更新 | AI Lab |
| Validated Need | 纳入 Sprint 规划 | AI Lab |

**转化动作**:
1. 创建对应 Issue
2. 标记标签 (bug/enhancement/question)
3. 评估是否进入下一轮迭代

---

## 3) 反馈处理最小流程

```
收到反馈
    ↓
[是否是重复?]
    ├─ Yes → 合并到已有 Issue
    └─ No → 继续
    ↓
[分类]
    ├─ Bug → 创建 Issue (bug)
    ├─ Feature → 创建 Issue (enhancement) + 评估
    ├─ Question → 回复 + 加入 FAQ
    └─ Other → 记录待定
    ↓
[优先级评估]
    ├─ P0 (影响核心) → 立即处理
    ├─ P1 (重要) → 下一 Sprint
    └─ P2 (一般) → 积压池
    ↓
[转化完成]
```

---

## 4) 当前 Feedback Pack

### 2026-03-13 Feedback Pack

```markdown
# Feedback Pack - 2026-03-13

## 项目
agent-memory

## 痛点
- 轻量级 memory 库需求
- LangChain 过于复杂

## 反馈问题
1. 你使用 agent-memory 的主要场景是什么?
2. 你愿意为哪些功能付费?
3. 你觉得最需要改进的是什么?

## 链接
- Issue: https://github.com/.../issues
- Survey: docs/feedback/SURVEY.md
- RFC: docs/feedback/RFC_TEMPLATE.md
```

---

## 5) 验证检查点

| 检查点 | 状态 |
|--------|------|
| Issue 模板存在 | ✅ docs/feedback/ |
| Discussion stub 存在 | 🔄 待创建 |
| Feedback Pack 今日存在 | 🔄 待创建 |
| 流程文档存在 | ✅ 本文件 |

---

## 下一步行动

- [ ] 创建 `docs/feedback/discussions_stub.md`
- [ ] 创建 `docs/feedback/packs/2026-03-13.md`
- [ ] 验证现有反馈入口可访问

---

*Feedback pipeline: 2026-03-13*
