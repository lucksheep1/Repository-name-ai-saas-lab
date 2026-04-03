# Skills Registry (技能资产化目录)

**更新日期**: 2026-03-12
**版本**: v3.0 (Evidence-First + Mainline Focus)

---

## 目录索引

### 0. Archive (归档)

- `skills/AI/` - 归档技能别名（触发词：用AI归档）
- `skills/archive-ingest/` - 文档统一归档技能

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
- `skills/feedback/` - 反馈收集 (playbook/snippets/checklist) ⭐
- `skills/competition/` - 竞品分析 (playbook/snippets/checklist) ⭐
- `skills/promotion/` - 推广策略 (playbook/snippets/checklist) ⭐

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

## Evidence-First v3 规则

### 合规 Evidence (只允许三类)
1. **竞品/替代方案主页** (PyPI/NPM/GitHub repo) - 用于"存在性"
2. **竞品 issue/discussion/PR** (链接或编号) - 用于"痛点/需求"
3. **官方文档/规范** (链接) - 用于"限制/复杂性"

### 禁止计入 Evidence
- 我们自己的仓库链接
- 投稿入口 (HN submit, Twitter intent)
- "我推断/README归因" (除非有 issue/discussion 佐证)

### 硬门槛
- 每个关键问题 ≥3 条合规 Evidence
- 不足则标记 MISSING + 检索计划
- "本地 examples 可运行" 只能写 Verification

---

## Mainline 规则

### 72h 强制锁定
- 只允许深挖 1 个主线项目
- 其他项目进入 Maintenance 模式 (只修 bug/文档/测试)

### Promising 上限
- 名额上限 = 2 (含主线)
- 硬条件: README Quick Demo + VERIFICATION.md + ≥3 合规 Evidence

---

## 使用规则

1. **遇到新问题** → 先查 skills/index.md 是否已有
2. **无则新增** → 写成 playbook.md + snippets.md + checklist.md
3. **每轮 Scout/Scanner** → 必须产出 Research Pack (≥3 合规 Evidence)
4. **任何"已解决"** → 必须对应新增/更新 skills 条目

---

## 维护记录

- 2026-03-11: 初始化 skills 目录
- 2026-03-12: v2.0 升级 - Evidence-First + Skill Registry
- 2026-03-12: v3.0 升级 - Mainline Focus + 三件套 (feedback/competition/promotion)

---

## 当前 Active 项目

| 项目 | 状态 | 证据数 |
|------|------|--------|
| agent-memory | Mainline 🔒 | 3/3 (合规) |
