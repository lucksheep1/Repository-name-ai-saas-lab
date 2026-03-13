# Feedback Triage Rules

**Generated**: 2026-03-13
**Project**: agent-memory

---

## 反馈分类体系

### 标签 (Labels)

| 标签 | 说明 | 颜色 |
|------|------|------|
| bug | 缺陷/错误 | red |
| enhancement | 功能增强 | blue |
| question | 问题咨询 | green |
| documentation | 文档相关 | yellow |
| use-case | 使用场景分享 | purple |
| wontfix | 不会修复 | gray |

### 优先级 (Priority)

| 优先级 | 说明 | 响应时间 |
|--------|------|----------|
| P0 | 影响核心功能，必须修复 | 24h |
| P1 | 重要功能，纳入下一迭代 | 48h |
| P2 | 改进建议，积压池 | 1 周 |

---

## 分类流程

```
收到反馈
    ↓
[判断类型]
    ├─ 报告错误 → bug
    ├─ 请求功能 → enhancement
    ├─ 问问题 → question
    ├─ 文档问题 → documentation
    └─ 分享经验 → use-case
    ↓
[判断优先级]
    ├─ 无法使用 → P0
    ├─ 功能缺失 → P1
    └─ 锦上添花 → P2
    ↓
[分配处理]
    → triage_board.md
    → feedback_to_iteration.md (如果开始闭环)
```

---

## 常见反馈归因

### Bug 归因

| 症状 | 归因 | 优先级 |
|------|------|--------|
| 安装失败 | 依赖问题 | P0 |
| 运行报错 | 代码缺陷 | P0/P1 |
| 结果不符合预期 | 逻辑问题 | P1 |

### Feature 归因

| 需求 | 归因 | 优先级 |
|------|------|--------|
| 新存储后端 | 功能缺失 | P1 |
| 新 API | 功能缺失 | P2 |
| 性能优化 | 体验改进 | P2 |

### UseCase 归因

| 场景 | 价值 | 处理 |
|------|------|------|
| Chatbot | 高 | 纳入示例 |
| Agent | 高 | 纳入示例 |
| 其他 | 中 | 记录观察 |

---

## 闭环触发条件

当满足以下任一条件时，启动闭环：

1. **Bug**: P0 级别，必须修复
2. **Feature**: 多人请求 (≥2) 或高价值
3. **UseCase**: 有代表性的新场景

---

## 闭环流程

```
选择目标反馈
    ↓
[归因分析]
    - 痛点是什么？
    - 根因是什么？
    ↓
[需求拆解]
    - 拆成具体任务
    - 评估工作量
    ↓
[实现/修复]
    - 写代码/改文档
    - commit
    ↓
[版本记录]
    - 更新 RELEASE.md
    - 标记版本号
    ↓
[反馈者通知]
    - 回复反馈者
    - 说明已处理
```

---

## 处理时间线

| 类型 | 确认 | 处理 | 关闭 |
|------|------|------|------|
| Bug P0 | 2h | 24h | 48h |
| Bug P1 | 4h | 48h | 72h |
| Enhancement | 24h | 1周 | 2周 |
| Question | 24h | 48h | 1周 |
| UseCase | 1周 | 2周 | 3周 |

---

## 输出文件

- `analysis/triage_board.md` - 当前待处理反馈
- `analysis/feedback_inbox.md` - 所有收到的反馈
- `analysis/feedback_to_iteration.md` - 闭环记录

---
