# archive-ingest

文档统一归档技能。当用户发送触发指令时激活，按《文档录入标准 v1》执行。

---

## 目标飞书知识库（已验证）

| 配置项 | 值 |
|--------|-----|
| 目标 Space | 7522776428406849538 |
| 根节点 | SI4kw3rLAiZEVkkF4pfcidVOnQg |
| 知识库入口 | https://my.feishu.cn/wiki/SI4kw3rLAiZEVkkF4pfcidVOnQg |
| 一级目录 | 按作者/来源创建为飞书 wiki 节点 |
| 二级文档 | 按日期创建为飞书文档 |

**权限状态：** 77项已授权（docx:document:create/write/read, wiki:wiki 等），链路完整验证通过。

---

## 适用输入

| 类型 | 描述 |
|------|------|
| 纯文字 | 消息正文直接作为内容 |
| 链接 | HTTP/HTTPS URL |
| PDF | PDF 文件 |
| 截图/图片 | 截图或图片附件（png/jpg/gif/webp） |

---

## 归档标准 vs 主落点

```
归档标准（必须遵循）：定义了"什么必须写入、什么必须校验"

主落点（飞书文档）：
  一级节点：feishu_wiki create（title = 作者/来源，parent = 根节点）
  二级文档：feishu_doc create → write → feishu_doc read（全链路）
  知识库入口：https://my.feishu.cn/wiki/SI4kw3rLAiZEVkkF4pfcidVOnQg

本地备份（可选，非默认）：
  仅在飞书文档归档完成后执行
  路径：~/.openclaw/workspace/archive/[作者或来源]/[YYYY-MM-DD].md
  状态字段：本地备份：✅ 已写入 / 未执行

飞书消息通知（可选辅助）：
  归档完成后可发送通知
  不是归档完成的标志，不得以通知替代归档
```

**归档完成的唯一标志：飞书文档 feishu_doc read-back 通过。**

---

## 执行流程

### Step 1：识别输入类型

| 类型 | 判断依据 |
|------|----------|
| 纯文字 | 消息正文即为内容 |
| 链接 | 消息含 URL |
| PDF | 收到文件路径或文件上传 |
| 截图/图片 | 收到媒体附件 |

### Step 2：内容提取

| 类型 | 提取方式 |
|------|----------|
| 纯文字 | 直接使用消息正文 |
| 链接 | web_fetch 抓取页面文本 |
| PDF | PDF 解析提取文本 |
| 截图/图片 | image 工具 → 保留原始识别文本输出（不经摘要加工） |

### Step 3：确认/创建一级目录（飞书 wiki 节点）

目标 Space 根节点：`SI4kw3rLAiZEVkkF4pfcidVOnQg`

```
feishu_wiki create：
  space_id: 7522776428406849538
  parent_node_token: SI4kw3rLAiZEVkkF4pfcidVOnQg
  title: [作者/来源名称]
  obj_type: docx

返回：node_token（后续写入用）+ obj_token（文档 ID）
```

- 已存在的一级目录（同一 space 内判断是否重复）：直接使用现有 node_token
- 不存在的一级目录：**必须先向用户确认**，未经确认不得创建

### Step 4：创建并写入二级文档（飞书 doc）

```
feishu_doc create：
  title: [YYYY-MM-DD] [标题/来源]
  folder_token: [Step 3 返回的 node_token]

feishu_doc write：
  doc_token: [Step 3 返回的 obj_token]
  content: [完整文档内容，含原文层+摘要层+复核标记]
```

文档正文模板：

```markdown
# [归档日期] [输入类型] [标题/来源]

**来源：** [发布者 / URL / 文件名]
**归档日期：** YYYY-MM-DD HH:MM
**输入类型：** 纯文字 / 链接 / PDF / 截图
**飞书文档路径：** doc_token: [来自 feishu_doc create 的返回值]
**本地备份：** 已写入 / 未执行（可选）

---

## 原文 / 原始识别文本

[全文粘贴，不做删减。不允许以"见摘要"代替。]
[若无法获取：填写"未获取 / 识别失败 + 原因"]

---

## 摘要

[有则填，无则填"无"。禁止留空。]

---

## 复核标记

- read-back 通过：✅ / ❌
- 原文/OCR 首句：[实际读取的前50字，逐字copy]
- 异常说明：[有则填，无则填"无"]

---
*录入完成时间: YYYY-MM-DD HH:MM*
```

### Step 5：read-back 复核（必须）

```
feishu_doc read：
  doc_token: [Step 3 返回的 obj_token]
```

验证：
1. 内容层非空
2. 返回内容与预期一致

read-back 必须提供"原文/OCR 首句"作为可观察证据，不得在 read-back 之前报告"完成"。

### Step 6：更新总索引 + 本地备份（可选）

总索引 `archive/index.md` 追加本次归档的飞书文档链接（doc_token / URL）。

飞书文档归档完成后，可选择写入本地备份：`archive/[作者或来源]/[YYYY-MM-DD].md`。

---

## 停止与确认条件

以下情况必须先向用户确认，不得自行推进：

1. 需要新增一级目录（飞书 wiki 节点不存在）时
2. 内容层为空，无法提取原文/OCR 文本时
3. 链接 404 或权限限制，无法获取页面内容时
4. read-back 失败，文档内容与预期不符时
5. 飞书文档 create/write 失败时——必须报告异常，不得以本地 archive 替代主落点

---

## 回报字段（完成后必须提供）

```
✅ 文档录入完成

飞书文档：✅ 已归档（doc_token: xxx）
飞书文档 URL：https://my.feishu.cn/wiki/[node_token]
本地备份：✅ 已写入 / 未执行（可选）
总索引：index.md（✅ 已更新）
输入类型：[纯文字/链接/PDF/截图]
作者/来源：[实际作者名 或 来源名 或 待确认]
内容层：✅ 已写入（共 N blocks）/ ❌ 缺失
原文/OCR 首句：[feishu_doc read 返回的前50字，逐字copy]
复核：✅ read-back 通过 / ❌ 未通过
摘要：✅ 已写入 / 无
⚠️ 异常说明：[无]
```

---

## 禁止行为

- 不得在 read-back 之前报告"完成"
- 不得以摘要替代内容层
- 不得未经确认自行创建新一级目录（飞书 wiki 节点）
- 不得跳过 image 工具原始输出直接写摘要
- 不得以本地 archive 替代飞书文档作为主落点
- 不得以飞书消息通知替代飞书文档归档完成
