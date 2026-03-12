# Competition Analysis Checklist

## 验收清单

### 竞品识别
- [ ] 确定直接竞品 (功能相似)
- [ ] 确定间接竞品 (解决相似问题)
- [ ] 列出所有竞品及主页链接

### Evidence 收集
- [ ] 每个竞品有主页链接 (PyPI/NPM/GitHub)
- [ ] 每个竞品有痛点证据 (issue/discussion)
- [ ] 至少 3 条合规 Evidence

### 差异化分析
- [ ] 对比表已完成
- [ ] 差异化点有 Evidence 支撑
- [ ] 结论区分 "evidence-based" vs "hypothesis"

### 合规性检查
- [ ] Evidence 无本仓库链接
- [ ] Evidence 无投稿入口 (HN submit, Twitter intent)
- [ ] Evidence 都是外部可点击链接

### 输出检查
- [ ] Research Pack 已生成
- [ ] 对比表在 playbook 或 snippets 中
- [ ] 无效 Evidence 已迁移到 Promotion section

---

## 验证命令

```bash
# 检查竞品链接
curl -I https://pypi.org/project/<package>/

# 检查 GitHub 仓库
curl -I https://github.com/<org>/<repo>

# 检查 issues
curl -I https://github.com/<org>/<repo>/issues
```

---

## 常见错误

| 错误 | 修复 |
|------|------|
| Evidence 写自己仓库 | 删除，保留竞品链接 |
| 写 HN submit 链接 | 移到 Promotion section |
| 写 Twitter intent | 移到 Promotion section |
| "我推断" 类描述 | 删除或标记为 hypothesis |
| 不足 3 条 Evidence | 标记 MISSING + 检索计划 |
