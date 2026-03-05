---
name: tencent-docs
description: 腾讯文档，提供完整的腾讯文档操作能力。当用户需要操作腾讯文档时使用此skill，包括：(1) 创建各类在线文档（智能文档、Word、Excel、幻灯片、思维导图、流程图）(2) 查询、搜索文档空间与文件 (3) 管理空间节点、文件夹结构 (4) 读取文档内容 (5) 编辑操作智能表。
homepage: https://docs.qq.com/home
metadata: {"openclaw":{"requires":{"env":["TENCENT_DOCS_TOKEN"]},"primaryEnv":"TENCENT_DOCS_TOKEN","category":"tencent","tencentTokenMode":"custom","tokenUrl":"https://docs.qq.com/open/document/mcp/get-token/","emoji":"📝"}}
---

# 腾讯文档 MCP 使用指南

腾讯文档 MCP 提供了一套完整的在线文档操作工具，支持创建、查询、编辑多种类型的在线文档。

## 📚 详细参考文档

如需查看每个工具的详细调用示例、参数说明和返回值说明，请参考：
- `references/api_references.md` - 包含所有工具的完整调用示例、参数说明、返回值说明及 API 结构、枚举值说明

## ⚙️ 配置要求

### 获取 Token

1. 访问 [https://docs.qq.com/open/document/mcp/get-token/](https://docs.qq.com/open/document/mcp/get-token/) 获取你的 Token
2. 登录后复制个人 Token
3. 在 OpenClaw 中配置环境变量 `TENCENT_DOCS_TOKEN`

> ⚠️ **如果用户未配置 Token**，请引导用户访问上方链接获取 Token，否则所有工具调用将返回鉴权失败。

### MCP 服务地址

- **访问地址**：`https://docs.qq.com/openapi/mcp`

## 🚀 快速开始（首次使用必读）

**首次使用前，必须先完成初始化配置**，运行 setup.sh 自动完成 MCP 服务注册：

```bash
bash setup.sh
```

> setup.sh 会自动将腾讯文档 MCP 服务注册到 mcporter，并验证配置是否成功。
> 如果未执行 setup，所有工具调用将无法找到 `tencent-docs` 服务。

### 验证配置

```bash
mcporter list | grep tencent-docs
```

---

## 🔧 调用方式

腾讯文档 MCP 的标准配置名称为 **`tencent-docs`**，通过内置 MCP Client 直接调用工具：

```
mcp: tencent-docs
tool: <工具名称>
arguments: { ... }
```

### 支持的工具完整列表

> ⚠️ **以下工具列表仅供参考，实际可用工具以调用 `tools/list` 接口返回结果为准。**
>
> 获取最新工具列表：
> ```
> mcp: tencent-docs
> method: tools/list
> ```

| 工具名称 | MCP 调用格式 | 功能说明 |
|---------|-------------|---------|
| create_smartcanvas_by_markdown | `create_smartcanvas_by_markdown` | ⭐ 创建智能文档（首选） |
| create_excel_by_markdown | `create_excel_by_markdown` | 创建 Excel 表格 |
| create_slide_by_markdown | `create_slide_by_markdown` | 创建幻灯片 |
| create_mind_by_markdown | `create_mind_by_markdown` | 创建思维导图 |
| create_flowchart_by_mermaid | `create_flowchart_by_mermaid` | 创建流程图 |
| create_word_by_markdown | `create_word_by_markdown` | 创建 Word 文档 |
| query_space_node | `query_space_node` | 查询空间节点 |
| create_space_node | `create_space_node` | 创建空间节点 |
| delete_space_node | `delete_space_node` | 删除空间节点 |
| search_space_file | `search_space_file` | 搜索空间文件 |
| get_content | `get_content` | 获取文档内容 |
| batch_update_sheet_range | `batch_update_sheet_range` | 批量更新表格 |
| create_smartcanvas_element | `create_smartcanvas_element` | 追加智能文档内容 |
| smartsheet.* | 见下方第 4 节 | 智能表格操作（工作表/视图/字段/记录），详见 `references/smartsheet_references.md` |

**详细调用示例请参考：`references/api_references.md`**

## ⭐ 重要：文档类型选择指南

> **首选推荐：智能文档（smartcanvas）**
>
> 在创建文档时，**优先使用 `create_smartcanvas_by_markdown`** 创建智能文档，原因如下：
> - 📝 排版效果更美观，自动优化布局
> - 🎨 支持更丰富的格式（标题、段落、列表、表格、代码块、引用、图片等）
> - 🔧 支持后续通过 `create_smartcanvas_element` 追加内容
> - 📱 跨平台显示效果一致

### 文档类型选择决策树

```
需要创建什么类型的内容？
│
├─ 通用文档内容（报告、笔记、文章等）
│   └─ ✅ 使用 create_smartcanvas_by_markdown（首选）
│
├─ 数据表格（需要计算、筛选、统计）
│   └─ ✅ 使用 create_excel_by_markdown
│
├─ 演示文稿（需要逐页展示、投影演示）
│   └─ ✅ 使用 create_slide_by_markdown
│
├─ 层次化知识整理（知识图谱、大纲）
│   └─ ✅ 使用 create_mind_by_markdown
│
├─ 流程/架构展示（流程图、时序图）
│   └─ ✅ 使用 create_flowchart_by_mermaid
│
├─ 结构化数据管理（多视图、字段管理、看板）
│   └─ ✅ 使用 smartsheet.* 工具（详见 `references/smartsheet_references.md`）
│
└─ 传统 Word 格式导出需求
    └─ 使用 create_word_by_markdown（仅在明确需要时）
```

## 支持的文档类型

| 类型 | doc_type | 推荐度 | 说明 |
|------|----------|--------|------|
| **智能文档** | smartcanvas | ⭐⭐⭐ **首选** | 排版美观，支持丰富组件 |
| Excel | excel | ⭐⭐⭐ | 数据表格专用 |
| 幻灯片 | slide | ⭐⭐⭐ | 演示文稿专用 |
| 思维导图 | mind | ⭐⭐⭐ | 知识图谱专用 |
| 流程图 | flowchart | ⭐⭐⭐ | 流程展示专用 |
| Word | word | ⭐⭐ | 传统格式，排版一般 |
| 收集表 | form | ⭐⭐ | 表单收集 |
| 智能表格 | smartsheet | ⭐⭐⭐ | 高级结构化表格，支持多视图、字段管理 |
| 白板 | board | ⭐⭐ | 在线白板 |

## 工具列表

> 📖 所有工具的完整调用示例、参数说明和返回值说明，请查阅 `references/api_references.md`
>
> ⚠️ **此 skill 中的工具列表仅作使用指导，实际可用工具以调用 `tools/list` 接口返回结果为准。** 如遇工具不存在或参数不符，请先执行 `tools/list` 获取最新工具定义。

### 1. 创建文档类

#### ⭐ create_smartcanvas_by_markdown（首选）

**通用文档首选工具**，通过 Markdown 创建智能文档，排版美观，支持所有 Markdown 基本结构。

**适用场景**：
- 📄 文档、报告、笔记、文章
- 📋 会议纪要、方案说明
- 📚 技术文档、教程
- 🗒️ 任何需要美观排版的内容

**支持 `parent_id` 参数**：可指定父节点 ID，将文档创建到指定目录下；不填则在根目录创建。

> 📖 调用示例请参考：`references/api_references.md` - create_smartcanvas_by_markdown

#### create_excel_by_markdown

通过 Markdown 表格创建 Excel，适用于需要数据计算、筛选的场景。

**适用场景**：数据报表、统计表格、需要公式计算的场景

**支持 `parent_id` 参数**：可指定父节点 ID，将文档创建到指定目录下；不填则在根目录创建。

> 📖 调用示例请参考：`references/api_references.md` - create_excel_by_markdown

#### create_slide_by_markdown

通过 Markdown 创建幻灯片，遵循特定层级结构（`#` 主标题 → `##` 章节 → `###` 页面 → `-` 段落 → 缩进子项正文）。

**适用场景**：演示文稿、项目汇报、培训材料

**支持 `parent_id` 参数**：可指定父节点 ID，将文档创建到指定目录下；不填则在根目录创建。

> 📖 调用示例请参考：`references/api_references.md` - create_slide_by_markdown

#### create_mind_by_markdown

通过 Markdown 创建思维导图，使用标题层级和列表嵌套表示结构。

**适用场景**：知识图谱、大纲整理、头脑风暴

**支持 `parent_id` 参数**：可指定父节点 ID，将文档创建到指定目录下；不填则在根目录创建。

> 📖 调用示例请参考：`references/api_references.md` - create_mind_by_markdown

#### create_flowchart_by_mermaid

通过 Mermaid 语法创建流程图，mermaid 字段内容必须全部使用英文。

**适用场景**：流程图、时序图、架构图

**支持 `parent_id` 参数**：可指定父节点 ID，将文档创建到指定目录下；不填则在根目录创建。

> 📖 调用示例请参考：`references/api_references.md` - create_flowchart_by_mermaid

#### create_word_by_markdown

通过 Markdown 创建 Word 文档。**注意：仅在用户明确要求 Word 格式时使用，否则请使用 smartcanvas**。

**支持 `parent_id` 参数**：可指定父节点 ID，将文档创建到指定目录下；不填则在根目录创建。

> 📖 调用示例请参考：`references/api_references.md` - create_word_by_markdown

### 2. 空间管理类

#### query_space_node

查询空间节点树结构，获取文件夹和文档列表。支持分页，每页返回 20 条。

> 📖 调用示例请参考：`references/api_references.md` - query_space_node

#### create_space_node

在空间中创建新节点，支持创建文件夹（`wiki_folder`）、在线文档（`wiki_tdoc`）、链接（`link`）。

> 📖 调用示例请参考：`references/api_references.md` - create_space_node

#### search_space_file

在空间内搜索文档，支持按关键词匹配标题和内容，支持分页，每页返回 40 条。

> ⚠️ 注意：仅能搜索到文档类节点（word、excel、slide 等），无法搜索文件夹；如需查找文件夹，请使用 `query_space_node` 遍历节点树。

> 📖 调用示例请参考：`references/api_references.md` - search_space_file

#### delete_space_node

删除空间中的指定节点，支持两种删除模式。

**删除类型（remove_type）**：
- `current`（默认）：仅删除当前节点，子节点自动挂载到上级节点
- `all`：删除当前节点及其所有子节点（⚠️ 谨慎使用，会递归删除所有子节点）

> 📖 调用示例请参考：`references/api_references.md` - delete_space_node

### 3. 文档操作类

#### get_content

获取文档完整内容，传入 `file_id` 返回文档正文文本。

> 📖 调用示例请参考：`references/api_references.md` - get_content

#### batch_update_sheet_range

批量更新表格单元格内容（仅适用于 Excel），数据从表格末尾追加，不覆盖已有内容。

> 📖 调用示例请参考：`references/api_references.md` - batch_update_sheet_range

#### create_smartcanvas_element

在已有智能文档中追加内容，这是 smartcanvas 的独特优势。

> 📖 调用示例请参考：`references/api_references.md` - create_smartcanvas_element

### 4. 智能表格（SmartSheet）操作类

智能表格支持对工作表、视图、字段、记录进行完整的增删改查操作，共 12 个工具（`smartsheet.*`）。

> 📖 **所有工具的完整说明（使用场景、字段定义、枚举值、参数示例）请查阅：`references/smartsheet_references.md`**
>
> 包含：工作表操作、视图操作、字段操作、记录操作，以及字段类型枚举、字段值格式参考、典型工作流示例。

## 常见工作流

### 创建通用文档（推荐方式）

```
1. 优先调用 create_smartcanvas_by_markdown 创建智能文档
2. 从返回结果中获取 file_id 和 url
3. 如需追加内容，调用 create_smartcanvas_element
```

### 组织文档到指定目录

1. 调用 `query_space_node` 查找目标文件夹
2. 调用 `create_space_node` 在目标位置创建文档节点（doc_type 优先选择 smartcanvas）

### 搜索并读取文档

1. 调用 `search_space_file` 搜索文档
2. 从结果中获取 `node_id`（即 `file_id`）
3. 调用 `get_content` 获取文档内容

### 智能表格操作工作流

#### 从零搭建任务管理表

```
1. 获取工作表列表 → smartsheet.list_tables（获取 sheet_id）
2. 添加字段（列）→ smartsheet.add_fields（任务名称、优先级、截止日期等）
3. 批量写入数据 → smartsheet.add_records
4. （可选）创建看板视图 → smartsheet.add_view（view_type=2）
```

#### 查询并更新数据

```
1. 获取工作表 → smartsheet.list_tables
2. 查询记录   → smartsheet.list_records（获取 record_id）
3. 更新记录   → smartsheet.update_records（传入 record_id 和新字段值）
```

> 📖 更多智能表格工作流示例请参考：`references/smartsheet_references.md` - 典型工作流示例

## 注意事项

- **默认使用 smartcanvas**：除非用户明确指定其他格式，否则创建文档时优先使用智能文档
- **创建文档时支持 `parent_id`**：所有 `create_*_by_markdown` 和 `create_flowchart_by_mermaid` 工具均支持 `parent_id` 参数，可将文档直接创建到指定目录；不填则在根目录创建
- **删除节点**：`delete_space_node` 默认仅删除当前节点（`remove_type=current`），使用 `all` 时会递归删除所有子节点，需谨慎
- Markdown 内容使用 UTF-8 格式，特殊字符无需转义
- 幻灯片必须遵循层级结构，每页包含 2-4 个段落标题
- 分页查询每页返回 20-40 条记录，使用 `has_next` 判断是否有更多
- `node_id` 同时也是文档的 `file_id`
- `create_flowchart_by_mermaid` 的 mermaid 内容必须全部使用英文
- **智能表格操作**：所有 smartsheet.* 工具都需要 `file_id` 和 `sheet_id`，操作前先调用 `smartsheet.list_tables` 获取 sheet_id
- **字段类型不可更新**：`update_fields` 时 field_type 不能修改，但必须传入原值
- **记录字段值格式**：不同字段类型的值格式不同，详见 `references/smartsheet_references.md` - 字段值格式参考