#!/usr/bin/env python3
"""
MCP Quick-Start - 一键生成 MCP Server 模板

Usage: python3 mcp-quickstart.py [template-name]

Templates:
  - basic     : 最简模板 (默认)
  - filesystem: 文件系统工具
  - git       : Git 操作工具
  - hybrid    : 混合工具集
"""

import json
import os
import sys
from pathlib import Path

TEMPLATES = {
    "basic": {
        "name": "basic",
        "description": "最简 MCP Server 模板",
        "files": {
            "package.json": json.dumps({
                "name": "mcp-server-basic",
                "version": "1.0.0",
                "type": "module",
                "description": "Basic MCP Server",
                "main": "index.js",
                "scripts": {
                    "start": "node index.js"
                },
                "dependencies": {
                    "@modelcontextprotocol/server": "^1.0.0",
                    "@modelcontextprotocol/sdk": "^1.0.0"
                }
            }, indent=2),
            "index.js": '''import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "basic-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("MCP Server running on stdio");
'''
        }
    },
    
    "filesystem": {
        "name": "filesystem",
        "description": "带文件系统操作的 MCP Server",
        "files": {
            "package.json": json.dumps({
                "name": "mcp-server-filesystem",
                "version": "1.0.0",
                "type": "module",
                "main": "index.js",
                "scripts": {"start": "node index.js"},
                "dependencies": {
                    "@modelcontextprotocol/server": "^1.0.0",
                    "@modelcontextprotocol/sdk": "^1.0.0"
                }
            }, indent=2),
            "index.js": '''import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolSchema, ListToolsSchema } from "@modelcontextprotocol/sdk/types.js";
import fs from "fs/promises";

const server = new Server(
  { name: "filesystem-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(CallToolSchema, async ({ params }) => {
  const { name, arguments: args } = params;
  try {
    if (name === "read_file") {
      const content = await fs.readFile(args.path, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }
    if (name === "list_files") {
      const files = await fs.readdir(args.path || ".");
      return { content: [{ type: "text", text: files.join("\\n") }] };
    }
    return { content: [{ type: "text", text: "Unknown tool" }], isError: true };
  } catch (error) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

server.setRequestHandler(ListToolsSchema, async () => ({
  tools: [
    { name: "read_file", description: "读取文件内容", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
    { name: "list_files", description: "列出目录文件", inputSchema: { type: "object", properties: { path: { type: "string" } } } }
  ]
}));

await server.connect(new StdioServerTransport());
console.error("Filesystem MCP Server running on stdio");
'''
        }
    },
    
    "git": {
        "name": "git",
        "description": "带 Git 操作的 MCP Server",
        "files": {
            "package.json": json.dumps({
                "name": "mcp-server-git",
                "version": "1.0.0",
                "type": "module",
                "main": "index.js",
                "scripts": {"start": "node index.js"},
                "dependencies": {
                    "@modelcontextprotocol/server": "^1.0.0",
                    "@modelcontextprotocol/sdk": "^1.0.0",
                    "simple-git": "^3.0.0"
                }
            }, indent=2),
            "index.js": '''import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolSchema, ListToolsSchema } from "@modelcontextprotocol/sdk/types.js";
import simpleGit from "simple-git";

const server = new Server({ name: "git-mcp-server", version: "1.0.0" }, { capabilities: { tools: {} } });

server.setRequestHandler(CallToolSchema, async ({ params }) => {
  const { name, arguments: args } = params;
  const git = simpleGit();
  try {
    if (name === "git_status") return { content: [{ type: "text", text: JSON.stringify(await git.status()) }] };
    if (name === "git_log") {
      const log = await git.log({ maxCount: args.count || 10 });
      return { content: [{ type: "text", text: log.all.map(l => `${l.hash.slice(0,7)} - ${l.message}`).join("\\n") }] };
    }
    return { content: [{ type: "text", text: "Unknown tool" }], isError: true };
  } catch (error) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

server.setRequestHandler(ListToolsSchema, async () => ({
  tools: [
    { name: "git_status", description: "获取 Git 状态", inputSchema: { type: "object", properties: {} } },
    { name: "git_log", description: "获取最近提交", inputSchema: { type: "object", properties: { count: { type: "number" } } } }
  ]
}));

await server.connect(new StdioServerTransport());
console.error("Git MCP Server running on stdio");
'''
        }
    },
    
    "hybrid": {
        "name": "hybrid",
        "description": "混合工具集 (filesystem + git + http)",
        "files": {
            "package.json": json.dumps({
                "name": "mcp-server-hybrid",
                "version": "1.0.0",
                "type": "module",
                "main": "index.js",
                "scripts": {"start": "node index.js"},
                "dependencies": {
                    "@modelcontextprotocol/server": "^1.0.0",
                    "@modelcontextprotocol/sdk": "^1.0.0",
                    "simple-git": "^3.0.0"
                }
            }, indent=2),
            "index.js": '''import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolSchema, ListToolsSchema } from "@modelcontextprotocol/sdk/types.js";
import fs from "fs/promises";
import simpleGit from "simple-git";
import https from "https";

const server = new Server({ name: "hybrid-mcp-server", version: "1.0.0" }, { capabilities: { tools: {} } });

server.setRequestHandler(CallToolSchema, async ({ params }) => {
  const { name, arguments: args } = params;
  try {
    if (name === "read_file") return { content: [{ type: "text", text: await fs.readFile(args.path, "utf-8") }] };
    if (name === "list_files") return { content: [{ type: "text", text: (await fs.readdir(args.path || ".")).join("\\n") }] };
    if (name === "git_status") return { content: [{ type: "text", text: JSON.stringify(await simpleGit().status()) }] };
    if (name === "http_get") {
      return await new Promise((resolve) => {
        https.get(args.url, (res) => {
          let data = "";
          res.on("data", chunk => data += chunk);
          res.on("end", () => resolve({ content: [{ type: "text", text: data.slice(0, 5000) }] }));
        }).on("error", e => resolve({ content: [{ type: "text", text: e.message }], isError: true }));
      });
    }
    return { content: [{ type: "text", text: "Unknown tool" }], isError: true };
  } catch (error) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

server.setRequestHandler(ListToolsSchema, async () => ({
  tools: [
    { name: "read_file", description: "读取文件", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
    { name: "list_files", description: "列出目录", inputSchema: { type: "object", properties: { path: { type: "string" } } } },
    { name: "git_status", description: "Git 状态", inputSchema: { type: "object", properties: {} } },
    { name: "http_get", description: "HTTP GET", inputSchema: { type: "object", properties: { url: { type: "string" } }, required: ["url"] } }
  ]
}));

await server.connect(new StdioServerTransport());
console.error("Hybrid MCP Server running on stdio");
'''
        }
    }
}


def main():
    template_name = sys.argv[1] if len(sys.argv) > 1 else "basic"
    template = TEMPLATES.get(template_name)
    
    if not template:
        print("MCP Quick-Start Generator\n")
        print("Usage: python3 mcp-quickstart.py [template]\n")
        print("Templates:")
        for t in TEMPLATES.values():
            print(f"  {t['name']:12} - {t['description']}")
        sys.exit(1)
    
    print(f"Generating {template['description']}...")
    
    for filename, content in template["files"].items():
        Path(filename).write_text(content)
        print(f"  Created: {filename}")
    
    print("\nDone! Run:")
    print("  npm install")
    print("  npm start")


if __name__ == "__main__":
    main()
