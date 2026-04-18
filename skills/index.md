# Skills Registry (技能资产化目录)

更新日期: 2026-04-14
版本: v3.2 (Disable Batch 1)

---

## 正式保留 Skill

### Archive
- `skills/archive-ingest/` - 文档统一归档 skill

### Opportunity Workflow
- `skills/site-tracker/` - 机会扫描 skill
- `skills/opportunity-research/` - 机会研究 skill

### Notify
- `skills/feishu-cron-notify/` - cron 完成后飞书通知 skill

---

## 观察保留 Skill

### GitHub
- `skills/github/` - GitHub CLI skill（唯一标识名: `github-cli`）
- `skills/github-api/` - GitHub API gateway skill（唯一标识名: `github-api`）

### Knowledge / Docs
- `skills/notion/` - Notion API skill
- `skills/tencent-docs/` - 腾讯文档 skill

### Utility / Channel
- `skills/weather/` - 天气查询 skill
- `skills/agent-browser/` - 浏览器自动化 skill
- `extensions/qqbot/skills/qqbot-cron/` - QQ 提醒 skill
- `extensions/qqbot/skills/qqbot-media/` - QQ 媒体发送 skill

---

## 已停用归档 Skill

以下 skill 已移出正式扫描路径，保留原始目录以便回滚：

- `AI` -> `/root/.openclaw/skills_disabled/batch1/AI.20260414-disabled/`
- `find-skills` -> `/root/.openclaw/skills_disabled/batch1/find-skills.20260414-disabled/`
- `summarize` -> `/root/.openclaw/skills_disabled/batch1/summarize.20260414-disabled/`
- `obsidian` -> `/root/.openclaw/skills_disabled/batch1/obsidian.20260414-disabled/`
- `tencentcloud-lighthouse-skill` -> `/root/.openclaw/skills_disabled/batch1/tencentcloud-lighthouse-skill.20260414-disabled/`
- `tavily-search` -> `/root/.openclaw/skills_disabled/batch1/tavily-search.20260414-disabled/`

批次说明见：`/root/.openclaw/skills_disabled/batch1/README.md`

---

## 非 Skill 资产（不应视为正式 Skill）

以下目录当前没有 `SKILL.md`，仅作为 playbook、checklist、snippets 或研究记录保留：

- `skills/competition/`
- `skills/feedback/`
- `skills/project_management/`
- `skills/promotion/`
- `skills/research_packs/`

---

## 已停用 / 兼容说明

- `/root/.openclaw/skills/feishu-cron-notify/`：已移出扫描路径，正式版本保留在 `workspace/skills/feishu-cron-notify/`

---

## 使用规则

1. 只把带 `SKILL.md` 的目录视为活动 skill。
2. 位于 `skills_disabled/` 的目录视为停用归档，不参与正式维护口径。
3. 没有 `SKILL.md` 的目录，只能按资料资产处理。
4. 引用 skill 时优先使用唯一标识名，避免同名漂移。
