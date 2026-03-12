# Promotion Checklist

## 发布前检查

### 项目准备
- [ ] README.md 完整 (Problem/Solution/Usage/Demo)
- [ ] Quick Demo 可运行并显示预期输出
- [ ] LICENSE 文件存在
- [ ] pyproject.toml 配置正确
- [ ] 依赖列表最小化

### PyPI 发布
- [ ] pyproject.toml 包含 build 配置
- [ ] 版本号已更新
- [ ] 描述文件 (README) 已配置
- [ ] 发布命令测试通过
- [ ] PyPI 页面可访问

### 社区推广
- [ ] Show HN 内容准备
- [ ] Twitter 文案准备
- [ ] Reddit 发帖内容准备

---

## 验证命令

```bash
# 检查 README Quick Demo
cd projects/agent-memory
python -c "from agent_memory import Memory; m = Memory(); m.add('test'); print(m.get_recent())"

# 检查 pyproject.toml
cat pyproject.toml | grep -E "name|version|description"

# 检查 LICENSE
head -3 LICENSE
```

---

## 常见错误

| 错误 | 修复 |
|------|------|
| Quick Demo 不完整 | 添加完整可运行代码 + 预期输出 |
| 依赖太多 | 最小化依赖，只保留必需 |
| README 太长 | 突出 Quick Demo，降低上手门槛 |
| 无 LICENSE | 添加 MIT/Apache 许可证 |
