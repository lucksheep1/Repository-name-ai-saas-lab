# Feedback Collection Playbook

## 目标
收集合规外部反馈证据，支撑 Promising/Scale 升级

---

## Evidence 合规要求

只接受三类 Evidence：
1. 竞品/替代方案主页 (PyPI/NPM/GitHub repo)
2. 竞品 issue/discussion/PR (链接或编号)
3. 官方文档/规范/高质量技术文章 (链接)

**禁止**:
- 我们自己的仓库链接
- 投稿入口 (HN submit, Twitter intent)
- 主观推断 (需 issue/discussion 佐证)

---

## 无 Token 降级模式

### 步骤

1. **创建反馈入口**
   - README.md 已有 Feedback 章节 ✓
   - 链接到 GitHub Issues

2. **创建反馈模板**
   - FAQ.md - 常见问题
   - SURVEY.md - 3 个关键问题 (谁用/痛点/愿付费)
   - RFC_TEMPLATE.md - 功能请求格式

3. **生成 Feedback Pack**
   - 路径: `docs/feedback/packs/YYYY-MM-DD.md`
   - 包含: 项目描述、痛点、反馈问题、链接

4. **记录合规 Evidence**
   - 路径: `analysis/feedback_evidence.md`
   - 每条证据需可追溯 (链接/编号 + commit)

---

## 验证方式

```bash
# 确认 Feedback 入口存在
grep -i "feedback" projects/agent-memory/README.md

# 确认 Pack 已生成
ls docs/feedback/packs/

# 验证 Evidence 合规性
# - 必须是外部链接 (非本仓库)
# - 必须是 issue/discussion/repo/文档
```

---

## 成功标准

- 72 小时内 ≥3 条合规 Evidence
- 每 24 小时至少 1 个反馈收集动作
- Evidence 必须可点击/可追溯

---

## 常见问题

Q: "本地 examples 可运行" 算 Evidence 吗?
A: 不算。这是 Verification，只能写在 Verification Delta。

Q: "用户说我们的产品好" 算 Evidence 吗?
A: 需要有链接/编号 (Twitter mention, GitHub comment, etc.) 否则不算合规 Evidence。
