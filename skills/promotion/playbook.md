# Promotion Playbook

## 目标
项目推广策略，提升曝光度

**注意**: 推广渠道不属于 Evidence，仅供参考

---

## 推广渠道

### 1. 技术社区
- **Hacker News**: Show HN
- **Reddit**: r/opensource, r/programming
- **Twitter/X**: 开发者社区

### 2. 包管理平台
- **PyPI**: 发布 Python 包
- **NPM**: 如果有 JS 组件

### 3. 内容营销
- 技术博客文章
- README 优化 (降低上手门槛)
- 示例代码

---

## 推广步骤

### 1. 准备发布
- [ ] 完善 README (Quick Demo)
- [ ] 添加 LICENSE
- [ ] 配置 pyproject.toml
- [ ] 添加 CI/CD (可选)

### 2. PyPI 发布
```bash
# 安装发布工具
pip install build twine

# 构建
python -m build

# 发布
twine upload dist/*
```

### 3. 社区发布
- [ ] 撰写 Show HN 内容
- [ ] 准备 Twitter 推广文案
- [ ] 准备 Reddit 发帖内容

---

## 验证方式

```bash
# 检查 README Quick Demo
grep -A5 "## Quick Start" projects/agent-memory/README.md

# 检查 pyproject.toml
cat projects/agent-memory/pyproject.toml

# 检查 LICENSE
cat projects/agent-memory/LICENSE
```

---

## 成功标准

- README 包含可运行的 Quick Demo
- 项目可通过 pip 安装
- 至少有 1 个推广渠道已执行
