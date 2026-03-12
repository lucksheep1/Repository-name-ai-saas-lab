# Competition Analysis Snippets

## 竞品搜索模板

### PyPI 搜索
```bash
# 搜索包信息
curl https://pypi.org/pypi/<package>/json | jq '.info.version, .info.requires_python, .info.dependencies'

# 搜索相关包
https://pypi.org/search/?q=<keyword>
```

### GitHub 搜索
```bash
# 搜索仓库
https://github.com/search?q=<keyword>+<use-case>&type=repositories

# 搜索 issues
https://github.com/<org>/<repo>/issues?q=<pain-keyword>

# 搜索 discussions
https://github.com/<org>/<repo>/discussions
```

---

## 竞品对比表模板

| 维度 | 本项目 | 竞品 A | 竞品 B |
|------|--------|--------|--------|
| 依赖数量 | 2 | 10+ | 5+ |
| 文件大小 | ~150 行 | 1000+ 行 | 500+ 行 |
| 框架依赖 | 无 | LangChain | 无 |
| 存储后端 | JSON/FAISS | 多 | Redis |
| 开源协议 | MIT | MIT | Apache |

---

## 痛点提取模板

### 从 Issue 提取
```
关键词: "complex", "heavy", "bug", "slow", "memory leak"
来源: GitHub Issues
链接: https://github.com/<repo>/issues?q=<keyword>
```

### 从 Discussion 提取
```
关键词: "alternative", "better", "simpler"
来源: GitHub Discussions
链接: https://github.com/<repo>/discussions
```

---

## 差异化定位模板

```markdown
## 差异化定位

### 竞品痛点
- 竞品 A: 依赖框架，太重
- 竞品 B: 配置复杂，上手难

### 我们优势
- 单一文件，无框架依赖
- 零配置，即装即用

### Evidence
- langchain 依赖: https://pypi.org/project/langchain/
- 我们的轻量: 本地验证
```
