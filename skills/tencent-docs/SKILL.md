---
name: tencent-docs
description: 腾讯文档操作能力。用于创建、查询、读取和编辑腾讯文档。仅在用户明确要求操作腾讯文档时使用。
homepage: https://docs.qq.com/home
metadata: {"openclaw":{"requires":{"env":["TENCENT_DOCS_TOKEN"]},"primaryEnv":"TENCENT_DOCS_TOKEN","category":"tencent","tencentTokenMode":"custom","tokenUrl":"https://docs.qq.com/open/document/mcp/get-token/","emoji":"📝"}}
---

# 腾讯文档 MCP 使用指南

## Required Dependency

- TENCENT_DOCS_TOKEN
- setup.sh
- references/api_references.md
- references/smartsheet_references.md

## Current Status

- TENCENT_DOCS_TOKEN: unconfigured in the current server shell
- setup.sh: present
- reference docs: present
- Fallback: none

## 配置要求

1. 访问 https://docs.qq.com/open/document/mcp/get-token/ 获取 Token
2. 配置环境变量 `TENCENT_DOCS_TOKEN`
3. 首次使用前执行：

```bash
bash setup.sh
```

## 验证配置

```bash
mcporter list | grep tencent-docs
```

## 调用方式

标准配置名称为 `tencent-docs`。
