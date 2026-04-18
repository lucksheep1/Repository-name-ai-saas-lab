---
name: archive-ingest
description: Structured document archiving skill. Writes verified source material into the Feishu knowledge base and requires read-back before reporting success.
---

# archive-ingest

## purpose

Archive source material into the target Feishu knowledge base with verifiable write and read-back steps.
The primary goal is stable ingestion, not summarization.

## when_to_use

- When the user asks to archive content into the Feishu knowledge base
- When the input is text, URL, PDF, screenshot, or image and the expected result is a Feishu document archive
- When the operator wants a verified write plus read-back record

## do_not_use_for

- General summarization without archival intent
- Pure notification tasks
- Tasks where Feishu is not the target destination
- Creating new top-level author/source nodes without user confirmation

## inputs

- plain_text: message body content
- url: HTTP or HTTPS link
- pdf_file: local PDF path or uploaded PDF
- image_input: screenshot or image attachment
- author_or_source: existing author/source node, or a user-confirmed new one

## outputs

- success status
- target location in Feishu
- write result
- read-back result
- failure reason if the run did not complete

## required_dependencies

- `feishu_doc` create / write / read / upload_image / upload_file
- `feishu_wiki` create when a confirmed new top-level node is needed
- OCR / image extraction path for screenshot or scanned PDF input
- access to the target Feishu knowledge base

## current_status

- feishu workflow status: documented as validated in this skill
- external dependency verification: not re-validated in this batch
- top-level node creation: confirmation required before use
- operational mode: documentation-level stable

## fallback

- If Feishu write or read-back fails: report failure, do not claim completion
- If author/source cannot be mapped confidently: ask for confirmation before writing
- If content extraction fails: report the extraction failure and stop
- If only local backup succeeds but Feishu does not: treat the archive as failed

## minimum_output_template

Use this minimum structure when reporting a run result:

```text
status: success | failure
target_location: <feishu_doc_url or unresolved>
write_result: success | failure | skipped
read_back_result: success | failure | skipped
failure_reason: <none or concrete reason>
```

## 目标飞书知识库（已验证）

| 配置项 | 值 |
|--------|-----|
| 目标 Space | 7522776428406849538 |
| 根节点 | SI4kw3rLAiZEVkkF4pfcidVOnQg |
| 知识库入口 | https://my.feishu.cn/wiki/SI4kw3rLAiZEVkkF4pfcidVOnQg |
| 一级目录 | 按作者/来源创建为飞书 wiki 节点 |
| 二级文档 | 按日期创建为飞书文档 |

权限状态：77项已授权（docx:document:create/write/read, wiki:wiki 等），链路完整验证通过。

## 已知一级目录（作者节点）

使用前必须确认作者归属。用户首次提供某作者内容时，先确认节点；后续同作者直接复用。

| 作者 | node_token | 说明 |
|------|-----------|------|
| 顾子明 | XS0Vwu5UZi3vDtkOTTucidV3n9c | 政事堂/子明私享汇 |
| 鉴茶财经院 | CztUwejITiqe8Xk5rIrc6taxn6b | 南院大王/100课程大法师（同一来源） |
| 洪灏 | TaS7wKOAriPdRAkeJRVcMxFYnbI | 市场策略师/怡广博晖资本 |
| 大盘剧本 | LA3OwENPJiXpxukWvsGcdJtanDh | 肥猪仔 |
| 看懂龙头股 | U0iswE4kXihobWkq1tucHVwunfe | 廖峥 |
| 专属群 | PP4GwYhsvim5xnkJShvcArdTn4f | |
| 拆姐星球 | EALfwSuFKiCU4ykhAjGc54DCnjg | |
| 丁辰灵 | DsXdwGI4jiNSyHkyhlVcNoyBnLg | |
| 珍大户 | AeQ0wBozai9GzBk6jU5cW05yncb | |
| 南半球聊财经 | GaehwGSxdiR10mkgyL8cgtBjnAf | |
| 智谷趋势 | KrypwGQAIiMvENkjzGqcD4jindD | |
| 知乎奥特之父 | OUw7wqHNCinqNLkWN8vcUhELnmb | |
| 思想钢印 | LxiMwEupsioLpkkhfKqcVnkjneb | |
| 斜杠睿 | PUzUw2s1BiLI7RkKN1Gc7Y5lnir | |
| 西风的罗盘 | OkjcwDQALiOFIUkVSFyc42nnnab | 2026-04-10新建 |
| 余说 | AtlwwZvTAicNuBkFXrPccvs1nDU | |
| 师涧道 | VvN9wO3jUiimqokycG6cvQJ7nbf | |
| 猫哥 | D55FwnGm9iYBjVkKU3NcTFWAn4f | |
| 沉默的螺旋 | K9ohwFhPci0Tb6kV5eac6xFenuf | |
| 胡斐 | EWYywqwFfiBHPvkhIG9czbuXndg | |
| 信息精选 | Hy76wusmli4GAVkt19Mc7SVinmc | |
| 马红漫 | Uqp2wcWkjiFePGkMg8Oc8gDgnof | 2026-04-09新建 |
| 米联储见闻 | XysFw2TcBiIOQuk1X4lcifOOnLh | 2026-04-10新建 |
| 洪灏星球 | YtAgwlBOkiqmlYksOkqcUikRnYA | |
| 大佳 | BZKBwpKO3iMOHBknz3Dccwkinbh | |
| 子明私享汇 | ACO2wTV2HiFaGCkzkB6c1exrnCe | 顾子明重名，已合并；仍有2个占位待清理 |

## 执行流程

### Step 1：识别输入类型

| 类型 | 判断依据 |
|------|----------|
| 纯文字 | 消息正文即为内容 |
| 链接 | 消息含 URL |
| PDF | 收到文件路径或文件上传 |
| 截图/图片 | 收到媒体附件 |

### Step 2：确认作者归属（重要）

不得猜测作者。用户首次提供某来源内容时，必须先确认归属哪个已知节点；同作者批量发送时直接复用节点 token。

### Step 3：内容提取

| 类型 | 提取方式 |
|------|----------|
| 纯文字 | 直接使用消息正文 |
| 链接 | web_fetch 抓取页面文本 |
| PDF | PDF 解析提取文本；扫描型 PDF 需转 PNG 后做 OCR |
| 截图/图片 | image 工具识别，保留原始识别文本 |

### Step 4：创建并写入二级文档

`feishu_doc create` 创建文档，并传 `folder_token`。
`feishu_doc write` 写入完整内容。
先 `write`，再 `upload_image`。

### Step 5：上传附件

使用 `feishu_doc upload_file` 或 `upload_image`。

### Step 6：read-back 复核（必须）

使用 `feishu_doc read` 验证：
1. 内容层非空
2. 返回内容与预期一致

### Step 7：更新总索引

归档完成后更新 `archive/index.md`。

## 停止与确认条件

以下情况必须先向用户确认，不得自行推进：
1. 需要新增一级目录时
2. 内容层为空，无法提取原文/OCR 文本时
3. 链接 404 或权限限制时
4. read-back 失败时
5. Feishu create/write 失败时
6. 作者归属不确定时

## 完成后回报字段

```text
✅ 文档录入完成

飞书文档：✅ 已归档（doc_token: xxx）
飞书文档 URL：https://feishu.cn/docx/[doc_token]
一级目录：[作者名]（node_token: xxx）
本地备份：✅ 已写入 / 未执行
输入类型：[纯文字/链接/PDF/截图]
内容层：✅ 已写入（共 N blocks）/ ❌ 缺失
原文/OCR 首句：[feishu_doc read 返回的前50字，逐字copy]
复核：✅ read-back 通过 / ❌ 未通过
⚠️ 异常说明：[有则填，无则填"无"]
```

## 禁止行为

- 不得在 write 之前 upload_image
- 不得在 read-back 之前报告完成
- 不得以摘要替代内容层
- 不得未经确认自行创建新一级目录
- 不得跳过 image 工具原始输出直接写摘要
- 不得以本地 archive 替代飞书主落点
- 不得以飞书消息通知替代归档完成
- 不得猜测作者归属
