# Skills Registry (技能资产化目录)

**更新日期**: 2026-03-12
**版本**: v2.0 (Evidence-First 升级)

---

## 目录索引

### 1. Feishu (飞书)
- `skills/feishu-doc/` - 飞书文档操作
- `skills/feishu-drive/` - 云空间管理
- `skills/feishu-wiki/` - 知识库操作
- `skills/feishu-perm/` - 权限管理

### 2. External Search (外部检索)
- `skills/tavily-search/` - Tavily AI 搜索
- `skills/summarize/` - URL/文件摘要
- `skills/agent-browser/` - 浏览器自动化
- `skills/find-skills/` - 技能发现

### 3. Project Management (项目管理)
- `skills/project_management/` - MVP 构建、Scale Gate
- `skills/feedback/` - 反馈收集模板

### 4. GitOps
- `skills/github/` - GitHub CLI 操作

### 5. Research (研究)
- `skills/research_packs/` - 外部检索记录
- **当前**: 2026-03-12-round65.md

### 6. Cloud (云服务)
- `skills/tencentcloud-lighthouse-skill/` - 腾讯云轻量应用服务器

### 7. Obsidian/Notion
- `skills/obsidian/` - Obsidian 笔记操作
- `skills/notion/` - Notion API

### 8. Weather
- `skills/weather/` - 天气查询

---

## Evidence-First 规则

### 证据优先级 (从高到低)
A. GitHub issue/discussion/PR (必须给链接或编号)
B. 官方文档/规范/README (给链接)
C. 论文/高质量技术博客 (给链接)

### 降级模式
网络受限时，生成 Research Pack 作为替代证据：
- 目标问题 (1句)
- 检索关键词 (中英各≥5个)
- 计划检索来源
- 已尝试的检索动作与结果
- 结论与不确定性
- 下一步

### 硬门槛
以下行为必须附 ≥3 条"可追溯证据"：
- 新机会进入 Builder
- Promising/Release 升级
- "市场/需求/痛点"结论
- "竞品更差/我更好"结论

---

## 使用规则

1. **遇到新问题** → 先查 skills/index.md 是否已有
2. **无则新增** → 写成操作手册 (playbook.md) + 最小代码 (snippets.md) + 验证清单 (checklist.md)
3. **每轮 Scout/Scanner** → 必须产出 Research Pack
4. **任何"已解决"** → 必须对应新增/更新 skills 条目

---

## 维护记录

- 2026-03-11: 初始化 skills 目录
- 2026-03-12: v2.0 升级 - Evidence-First + Skill Registry

---

## 当前 Active 项目

| 项目 | 状态 | 证据数 |
|------|------|--------|
| agent-memory | Promising 🔒 | 5/5 |
