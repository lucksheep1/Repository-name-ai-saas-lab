# Feedback Collection Checklist

## 验收清单

### 反馈入口检查
- [ ] README.md 包含 Feedback 章节
- [ ] Feedback 章节链接到 GitHub Issues
- [ ] Issue 模板已创建 (.github/ISSUE_TEMPLATE/)

### 反馈模板检查
- [ ] FAQ.md 存在且包含常见问题
- [ ] SURVEY.md 存在且包含 3 个关键问题
- [ ] RFC_TEMPLATE.md 存在且格式规范

### Evidence 合规性检查
- [ ] Evidence 只包含外部链接 (非本仓库)
- [ ] Evidence 来自 issue/discussion/repo/文档
- [ ] 每条 Evidence 有可点击链接或编号
- [ ] 无 "我推断" 类主观描述

### 记录检查
- [ ] Feedback Pack 已生成 (docs/feedback/packs/YYYY-MM-DD.md)
- [ ] evidence_evidence.md 已更新
- [ ] 每条证据有 commit 记录

### 时间检查
- [ ] 72 小时内 ≥3 条合规 Evidence
- [ ] 每 24 小时至少 1 个反馈动作

---

## 验证命令

```bash
# 检查 README Feedback 入口
grep -i "feedback" projects/agent-memory/README.md

# 检查 Issue 模板
ls .github/ISSUE_TEMPLATE/

# 检查 Feedback Packs
ls docs/feedback/packs/

# 检查 Evidence 记录
cat analysis/feedback_evidence.md
```

---

## 常见错误

| 错误 | 修复 |
|------|------|
| Evidence 写本仓库链接 | 删除，改用外部链接 |
| "我推断" 写入 Evidence | 删除，改为 "hypothesis" |
| 本地 examples 写入 Evidence | 移到 Verification Delta |
| 无效链接 (HN submit) | 移到 Promotion section |
