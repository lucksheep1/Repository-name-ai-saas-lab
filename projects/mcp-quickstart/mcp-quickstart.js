#!/usr/bin/env node

/**
 * MCP Quick-Start - 一键生成 MCP Server 模板
 * 
 * Usage: node mcp-quickstart.js [template-name]
 * 
 * Templates:
 *   - basic     : 最简模板 (默认)
 *   - filesystem: 文件系统工具
 *   - git       : Git 操作工具
 *   - hybrid    : 混合工具集
 */

const fs = require('fs');
const path = require('path');

const TEMPLATES = {
  basic: {
    name: 'basic',
    description: '最简 MCP Server 模板',
    files: {
      'package.json': JSON.stringify({
        name: "mcp-server-basic",
        version: "1.0.0",
        type: "module",
        description: "Basic MCP Server",
        main: "index.js",
        scripts: {
          start: "node index.js",
          test: "echo \\"No tests yet\\""
        },
        dependencies: {
          "@modelcontextprotocol/server": "^1.0.0",
          "@modelcontextprotocol/sdk": "^1.0.0"
        }
      }, null, 2),
      'index.js': `import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolSchema,
  ListResourcesSchema,
  ListToolsSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "basic-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("MCP Server running on stdio");
`
      }
    }
  },
  
  filesystem: {
    name: 'filesystem',
    description: '带文件系统操作的 MCP Server',
    files: {
      'package.json': JSON.stringify({
        name: "mcp-server-filesystem",
        version: "1.0.0",
        type: "module",
        description: "Filesystem MCP Server",
        main: "index.js",
        scripts: {
          start: "node index.js",
          test: "echo \\"No tests yet\\""
        },
        dependencies: {
          "@modelcontextprotocol/server": "^1.0.0",
          "@modelcontextprotocol/sdk": "^1.0.0"
        }
      }, null, 2),
      'index.js': `import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolSchema,
  ListToolsSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "fs/promises";
import path from "path";

const server = new Server(
  {
    name: "filesystem-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 注册工具: read_file
server.setRequestHandler(CallToolSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === "read_file") {
    try {
      const content = await fs.readFile(args.path, "utf-8");
      return { content: [{ type: "text", text: content }] };
    } catch (error) {
      return { content: [{ type: "text", text: \`Error: \${error.message}\` }], isError: true };
    }
  }
  
  if (name === "list_files") {
    try {
      const files = await fs.readdir(args.path || ".");
      return { content: [{ type: "text", text: files.join("\\n") }] };
    } catch (error) {
      return { content: [{ type: "text", text: \`Error: \${error.message}\` }], isError: true };
    }
  }
  
  return { content: [{ type: "text", text: "Unknown tool" }], isError: true };
});

// 列出可用工具
server.setRequestHandler(ListToolsSchema, async () => {
  return {
    tools: [
      {
        name: "read_file",
        description: "读取文件内容",
        inputSchema: {
          type: "object",
          properties: {
            path: { type: "string", description: "文件路径" }
          },
          required: ["path"]
        }
      },
      {
        name: "list_files",
        description: "列出目录文件",
        inputSchema: {
          type: "object",
          properties: {
            path: { type: "string", description: "目录路径 (默认当前目录)" }
          }
        }
      }
    ]
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Filesystem MCP Server running on stdio");
`
      }
    }
  },
  
  git: {
    name: 'git',
    description: '带 Git 操作的 MCP Server',
    files: {
      'package.json': JSON.stringify({
        name: "mcp-server-git",
        version: "1.0.0",
        type: "module",
        description: "Git MCP Server",
        main: "index.js",
        scripts: {
          start: "node index.js",
          test: "echo \\"No tests yet\\""
        },
        dependencies: {
          "@modelcontextprotocol/server": "^1.0.0",
          "@modelcontextprotocol/sdk": "^1.0.0",
          "simple-git": "^3.0.0"
        }
      }, null, 2),
      'index.js': `import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolSchema, ListToolsSchema } from "@modelcontextprotocol/sdk/types.js";
import simpleGit from "simple-git";

const server = new Server(
  { name: "git-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(CallToolSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const git = simpleGit();

  try {
    if (name === "git_status") {
      const status = await git.status();
      return { content: [{ type: "text", text: JSON.stringify(status, null, 2) }] };
    }
    if (name === "git_log") {
      const log = await git.log({ maxCount: args.count || 10 });
      return { content: [{ type: "text", text: log.all.map(l => \`\${l.hash.slice(0,7)} - \${l.message}\`).join("\\n") }] };
    }
    return { content: [{ type: "text", text: "Unknown tool" }], isError: true };
  } catch (error) {
    return { content: [{ type: "text", text: \`Error: \${error.message}\` }], isError: true };
  }
});

server.setRequestHandler(ListToolsSchema, async () => ({
  tools: [
    { name: "git_status", description: "获取 Git 状态", inputSchema: { type: "object", properties: {} } },
    { name: "git_log", description: "获取最近提交", inputSchema: { type: "object", properties: { count: { type: "number" } } } }
  ]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Git MCP Server running on stdio");
`
      }
    }
  },
  
  hybrid: {
    name: 'hybrid',
    description: '混合工具集 (filesystem + git + http)',
    files: {
      'package.json': JSON.stringify({
        name: "mcp-server-hybrid",
        version: "1.0.0",
        type: "module",
        description: "Hybrid MCP Server with FS + Git + HTTP",
        main: "index.js",
        scripts: {
          start: "node index.js"
        },
        dependencies: {
          "@modelcontextprotocol/server": "^1.0.0",
          "@modelcontextprotocol/sdk": "^1.0.0",
          "simple-git": "^3.0.0"
        }
      }, null, 2),
      'index.js': `import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolSchema, ListToolsSchema } from "@modelcontextprotocol/sdk/types.js";
import fs from "fs/promises";
import simpleGit from "simple-git";
import https from "https";

const server = new Server({ name: "hybrid-mcp-server", version: "1.0.0" }, { capabilities: { tools: {} } });

server.setRequestHandler(CallToolSchema, async ({ params }) => {
  const { name, arguments: args } = params;
  try {
    if (name === "read_file") {
      return { content: [{ type: "text", text: await fs.readFile(args.path, "utf-8") }] };
    }
    if (name === "list_files") {
      return { content: [{ type: "text", text: (await fs.readdir(args.path || ".")).join("\\n") }] };
    }
    if (name === "git_status") {
      return { content: [{ type: "text", text: JSON.stringify(await simpleGit().status(), null, 2) }] };
    }
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
    return { content: [{ type: "text", text: \`Error: \${error.message}\` }], isError: true };
  }
});

server.setRequestHandler(ListToolsSchema, async () => ({
  tools: [
    { name: "read_file", description: "读取文件", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
    { name: "list_files", description: "列出目录", inputSchema: { type: "object", properties: { path: { type: "string" } } } },
    { name: "git_status", description: "Git 状态", inputSchema: { type: "object", properties: {} } },
    { name: "http_get", description: "HTTP GET 请求", inputSchema: { type: "object", properties: { url: { type: "string" } }, required: ["url"] } }
  ]
}));

await server.connect(new StdioServerTransport());
console.error("Hybrid MCP Server running on stdio");
`
      }
    }
  }
};

// CLI 逻辑
function main() {
  const templateName = process.argv[2] || 'basic';
  const template = TEMPLATES[templateName];
  
  if (!template) {
    console.log(\`MCP Quick-Start Generator\\n\`);
    console.log(\`Usage: node mcp-quickstart.js [template]\\n\`);
    console.log(\`Templates:\`);
    Object.values(TEMPLATES).forEach(t => {
      console.log(\`  \${t.name.padEnd(12)} - \${t.description}\`);
    });
    process.exit(1);
  }
  
  console.log(\`Generating \${template.description}...\`);
  
  // 创建文件
  Object.entries(template.files).forEach(([filename, content]) => {
    fs.writeFileSync(filename, content);
    console.log(\`  Created: \${filename}\`);
  });
  
  console.log(\`\\nDone! Run:\`);
  console.log(\`  npm install\`);
  console.log(\`  npm start\`);
}

main();
