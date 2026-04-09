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

## 已知一级目录（作者节点）

> 使用前必须确认作者归属。用户首次提供某作者内容时，先确认节点；后续同作者直接复用。

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
| 余说 | AtlwwZvTAicNuBkFXrPccvs1nDU | |
| 师涧道 | VvN9wO3jUiimqokycG6cvQJ7nbf | |
| 猫哥 | D55FwnGm9iYBjVkKU3NcTFWAn4f | |
| 沉默的螺旋 | K9ohwFhPci0Tb6kV5eac6xFenuf | |
| 胡斐 | EWYywqwFfiBHPvkhIG9czbuXndg | |
| 信息精选 | Hy76wusmli4GAVkt19Mc7SVinmc | |
| 马红漫 | Uqp2wcWkjiFePGkMg8Oc8gDgnof | 2026-04-09新建 |
| 洪灏星球 | YtAgwlBOkiqmlYksOkqcUikRnYA | |
| 大佳 | BZKBwpKO3iMOHBknz3Dccwkinbh | |
| 子明私享汇 | ACO2wTV2HiFaGCkzkB6c1exrnCe | 顾子明重名，已合并；仍有2个占位待清理 |

---

## 适用输入

| 类型 | 描述 |
|------|------|
| 纯文字 | 消息正文直接作为内容 |
| 链接 | HTTP/HTTPS URL |
| PDF | PDF 文件（通常为图片扫描格式） |
| 截图/图片 | 截图或图片附件（png/jpg/gif/webp） |

---

## 归档标准 vs 主落点

```
归档标准（必须遵循）：定义了"什么必须写入、什么必须校验"

主落点（飞书文档）：
  一级节点：feishu_wiki create（title = 作者/来源，parent = 根节点）
  二级文档：feishu_doc create（folder_token=node_token）→ write → upload_image → read-back（全链路）
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

### Step 2：确认作者归属（重要！）

**不得猜测作者。** 用户首次提供某来源内容时，必须先确认归属哪个已知节点；同作者批量发送时直接复用节点 token。

确认清单：
1. 此作者是否在已知一级目录表中？→ 直接使用 node_token
2. 此作者是否未见过？→ **必须向用户确认**作者名和目录归属，再创建新节点
3. 用户是否指定了目录？→ 按用户指定执行

### Step 3：内容提取

| 类型 | 提取方式 |
|------|----------|
| 纯文字 | 直接使用消息正文 |
| 链接 | web_fetch 抓取页面文本 |
| PDF | PDF 解析提取文本（通常为图片扫描，需转 PNG 后用 image 工具识别） |
| 截图/图片 | image 工具 → 保留原始识别文本输出（不经摘要加工） |

**PDF 处理要点（必读）：**
- 大多数子明私享汇类 PDF 为图片扫描格式，`fitz.open().get_text()` 只能提取水印
- 标准流程：`fitz` 渲染 page → PNG → `image` 工具识别 → 获取完整文字
- PDF 有 XRef 错误不影响图片渲染，继续处理

### Step 4：创建并写入二级文档（飞书 doc）

```
feishu_doc create：
  title: [YYYY-MM-DD] [标题/来源]
  folder_token: [Step 3 确认的 node_token]   ← 必填！不填则落入云盘根目录

feishu_doc write：
  doc_token: [feishu_doc create 返回的 doc_token]
  content: [完整文档内容]
```

**图片处理顺序（重要，禁止颠倒）：**
1. `write`（文字内容）← 先写文字
2. `upload_image`（图片追加到文档末尾）← 后上传图片
3. **不得先 upload_image 再 write**，否则图片 block 会被文字内容整体覆盖

### Step 5：上传附件（PDF/图片）

```
feishu_doc upload_file（PDF）或 upload_image（图片）：
  doc_token: [Step 4 的 doc_token]
  file_path: [本地文件路径]
```

返回 file_token，在文档中记录供参考。

### Step 6：read-back 复核（必须）

```
feishu_doc read：
  doc_token: [Step 4 的 doc_token]
```

验证：
1. 内容层非空（block_count > 0）
2. 返回内容与预期一致

read-back 必须提供"原文/OCR 首句"作为可观察证据，不得在 read-back 之前报告"完成"。

### Step 7：更新总索引（归档完成后必须）

`archive/index.md` 追加本次归档记录：doc_token、URL、作者、标题、日期。

---

## 停止与确认条件

以下情况必须先向用户确认，不得自行推进：

1. 需要新增一级目录（飞书 wiki 节点不存在）时 → 先确认作者名
2. 内容层为空，无法提取原文/OCR 文本时 → 报告异常
3. 链接 404 或权限限制，无法获取页面内容时 → 报告异常
4. read-back 失败，文档内容与预期不符时 → 重新 write
5. 飞书文档 create/write 失败时 → 必须报告异常
6. 作者归属不确定时 → 先确认，不猜测

---

## 回报字段（完成后必须提供）

```
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

---

## 常见错误与应对

### 错误1：文档落入云盘根目录
**原因**：`feishu_doc create` 未传 `folder_token`。
**应对**：必须传 `folder_token=node_token`，node_token 来自 `feishu_wiki create` 或已知节点表。

### 错误2：`feishu_wiki spaces` 返回空
**原因**：Bot 未加入该 space，但 node_token 本身有效。
**应对**：直接用已知 node_token 调用 `feishu_doc create folder_token=xxx`，无需先查 spaces。

### 错误3：图片 block 被文字覆盖
**原因**：`upload_image` 在 `write` 之前执行。
**应对**：严格按 write → upload_image 顺序执行。

### 错误4：PDF 文字提取为空
**原因**：PDF 为图片扫描格式，`get_text()` 只能读到水印。
**应对**：用 `fitz` 渲染页面为 PNG，再用 `image` 工具识别文字。

---

## 禁止行为

- 不得在 write 之前 upload_image（会导致图片 block 被覆盖）
- 不得在 read-back 之前报告"完成"
- 不得以摘要替代内容层
- 不得未经确认自行创建新一级目录（飞书 wiki 节点）
- 不得跳过 image 工具原始输出直接写摘要
- 不得以本地 archive 替代飞书文档作为主落点
- 不得以飞书消息通知替代飞书文档归档完成
- 不得猜测作者归属，必须先确认
