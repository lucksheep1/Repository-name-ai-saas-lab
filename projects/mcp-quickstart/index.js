import { Server } from "@modelcontextprotocol/sdk/server/index.js";
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
    if (name === "list_files") return { content: [{ type: "text", text: (await fs.readdir(args.path || ".")).join("\n") }] };
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
