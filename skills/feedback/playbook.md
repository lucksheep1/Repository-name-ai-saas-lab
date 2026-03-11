# Feedback Collection Playbook

## 目标
收集外部反馈证据，支撑 Promising/Scale 升级

---

## 无 Token 降级模式

### 步骤

1. **创建反馈入口**
   - README.md 已有 Feedback 章节 ✓
   - 链接到 GitHub Issues

2. **创建反馈模板**
   - FAQ.md - 常见问题
   - SURVEY.md - 3 个关键问题（谁用/痛点/愿付费）
   - RFC_TEMPLATE.md - 功能请求格式

3. **生成 Feedback Pack**
   - 路径: `docs/feedback/packs/YYYY-MM-DD.md`
   - 包含: 项目描述、痛点、反馈问题、链接

4. **记录证据**
   - 路径: `analysis/feedback_evidence.md`
   - 每条证据需可追溯（文件路径 + commit）

---

## 验证方式

```bash
# 确认 Feedback 入口存在
grep -i "feedback" projects/agent-memory/README.md

# 确认 Pack 已生成
ls docs/feedback/packs/YYYY-MM-DD.md
```

---

## 成功标准

- 72 小时内 ≥5 条证据条目
- 每 24 小时至少 1 个反馈收集动作
