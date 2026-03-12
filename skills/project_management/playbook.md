# Project Management Playbook

## 目标
管理 AI SaaS Lab 项目生命周期：Scout → Scanner → Builder → Analyst → Evolution

---

## Scale Gate 模式

### 触发条件
- 项目进入 Promising 状态
- 锁定 72 小时只做主线迭代

### 执行步骤

1. **锁定主线**
   - 暂停其他项目 (STATUS = Archive)
   - 只允许 bug 修复/文档/测试

2. **Evidence Gate**
   - 72 小时内收集 ≥3 条外部反馈证据
   - 每 24 小时至少 1 个反馈收集动作

3. **里程碑检查**
   - Demo/示例
   - 集成例子
   - 发布变更

---

## 项目状态

| 状态 | 含义 | 升级条件 |
|------|------|---------|
| Experiment | 实验中 | 产出 MVP |
| Promising | 有潜力 | 证据 ≥3 + Score ≥40 |
| Scale | 可扩展 | 真实用户反馈 ≥3 |
| Archive | 已归档 | 暂停/放弃 |

---

## 验证命令

```bash
# 查看项目状态
cat projects/<project>/STATUS.md

# 查看 Scale Gate 状态
cat analysis/scale_gate_status.md

# 查看外部反馈证据
cat analysis/feedback_evidence.md
```

---

## 成功标准

- Scale Gate 期间: 只做主线迭代
- Evidence Gate: 72h 内 ≥3 条证据
- 每轮提交: 至少 1 个 git commit
