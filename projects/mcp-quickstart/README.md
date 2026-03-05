# MCP Quick-Start

一键生成 MCP Server 模板的 CLI 工具。

## Problem

MCP (Model Context Protocol) 生态正在爆发，但开发者不知道如何快速创建自己的 MCP server。现有方案：
- 官方文档示例零散
- 缺乏中文友好资源
- 无标准化项目结构

## Solution

提供 4 种模板，一键生成可运行的 MCP Server：
- `basic` - 最简模板 (~20 行)
- `filesystem` - 文件系统工具
- `git` - Git 操作工具
- `hybrid` - 混合工具集 (fs + git + http)

## Usage

```bash
# 进入项目目录
cd projects/mcp-quickstart

# 生成模板
python3 mcp-quickstart.py [template-name]

# 示例
python3 mcp-quickstart.py basic
python3 mcp-quickstart.py filesystem
python3 mcp-quickstart.py hybrid
```

## 验证

```bash
# 进入生成的模板目录
cd (模板目录)

# 安装依赖
npm install

# 启动测试 (需要与支持 MCP 的 AI 客户端配合)
npm start
```

## 包含的工具

### filesystem 模板
- `read_file` - 读取文件内容
- `list_files` - 列出目录文件

### git 模板
- `git_status` - 获取 Git 状态
- `git_log` - 获取最近提交

### hybrid 模板
- 全部 filesystem + git 工具
- `http_get` - HTTP GET 请求

## Limits

- 仅生成模板代码，需自行配置 AI 客户端
- 错误处理较简化，生产环境需加强

## Next

- [ ] 添加更多工具模板 (database, shell, etc.)
- [ ] 支持 TypeScript 模板
- [ ] 添加测试脚本
- [ ] 支持自定义工具参数

---
*Created: 2026-03-05*
*Status: Experiment*
