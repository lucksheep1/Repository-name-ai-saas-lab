# AI

> archive-ingest 的别名技能。触发词：`用AI归档`

---

## 触发指令

**`用AI归档`** — 等同于"按 archive-ingest 处理这条"

直接执行 archive-ingest SKILL.md 中的完整流程：

1. 识别输入类型（纯文字/链接/PDF/截图/图片）
2. 内容提取（原文层必须保留）
3. 确认/创建一级目录（飞书 wiki 节点，按作者/来源）
4. 写入飞书文档（feishu_doc create → write）
5. read-back 复核（必须）
6. 更新总索引 + 本地备份（可选）

---

## 目标飞书知识库

| 配置项 | 值 |
|--------|-----|
| 目标 Space | 7522776428406849538 |
| 根节点 | SI4kw3rLAiZEVkkF4pfcidVOnQg |
| 知识库入口 | https://my.feishu.cn/wiki/SI4kw3rLAiZEVkkF4pfcidVOnQg |

---

## 核心约束

- 主落点：飞书文档
- 一级目录：按作者/来源
- 新一级目录：必须先向用户确认
- 内容层必须保留，不能以摘要替代
- 没有 read-back 通过不得报告完成
- 本地 archive 为可选备份，不是主落点

---

## 完整执行标准

见 `skills/archive-ingest/SKILL.md`
