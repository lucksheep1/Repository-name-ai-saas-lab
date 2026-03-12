# Project Management Snippets

## 快速命令

### 查看项目状态
```bash
# 查看当前主线项目
cat HEARTBEAT.md | grep "主线项目"

# 查看 Scale Gate 状态
cat analysis/scale_gate_status.md

# 查看所有项目状态
ls projects/*/STATUS.md
```

### 切换主线
```bash
# 修改 STATUS.md
echo "# STATUS: Promising 🔒" > projects/<project>/STATUS.md

# 更新 Scale Gate
sed -i 's/主线项目:.*/主线项目: <project>/' analysis/scale_gate_status.md
```

### 创建新项目
```bash
# 初始化项目目录
mkdir -p projects/<project_name>
cd projects/<project_name>

# 创建必要文件
touch README.md STATUS.md OPPORTUNITY.md value_score.md experiment_log.md
```

### 收集反馈证据
```bash
# 添加反馈入口到 README
echo -e "\n## Feedback\n[Report Bug](https://github.com/...)" >> README.md

# 创建 Feedback Pack
cp docs/feedback/packs/template.md docs/feedback/packs/$(date +%Y-%m-%d).md
```

---

## 文件模板

### STATUS.md
```markdown
# STATUS: <Experiment|Promising|Scale|Archive>

**创建时间**: YYYY-MM-DD

**理由**:
- Score: XX/50
- 关键证据: ...

**下一步**:
- [ ] ...

---
*Status: <Experiment ✅|Promising ✅|Scale 🚀|Archive ❌>*
```

### OPPORTUNITY.md
```markdown
# Opportunity: <Name>

## Problem
<1-2 句描述>

## Evidence
- 证据1
- 证据2
- 证据3

## Existing Solutions
- 竞品1: 缺点
- 竞品2: 缺点

## Differentiation
<差异化点>
```
