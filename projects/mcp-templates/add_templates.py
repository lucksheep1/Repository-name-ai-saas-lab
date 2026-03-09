#!/usr/bin/env python3
"""Add new templates to MCP generator"""

with open('generator.py', 'r') as f:
    content = f.read()

# Old pattern to find
old = '- `send_template`: Send email from template (welcome, reminder, alert)\n"\n        }\n    }\n}\n\n\n\ndef create_project'

# New templates to add
new_templates = '''
    "firecrawl": {
        "description": "Web scraping with Firecrawl API",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Firecrawl Web Scraping"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import os, json, requests

app = Server("mcp-firecrawl")
API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")

@app.list_tools()
async def list_tools():
    return [
        Tool(name="scrape", description="Scrape a web page",
             inputSchema={"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}),
        Tool(name="crawl", description="Crawl a website",
             inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "limit": {"type": "integer", "default": 10}}, "required": ["url"]}),
        Tool(name="search", description="Search the web",
             inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]})
    ]

@app.call_tool()
async def call_tool(name, arguments):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        if name == "scrape":
            r = requests.post("https://api.firecrawl.dev/v1/scrape", json={"url": arguments["url"], "formats": ["markdown"]}, headers=headers)
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]
        elif name == "crawl":
            r = requests.post("https://api.firecrawl.dev/v1/crawl", json={"url": arguments["url"], "limit": arguments.get("limit", 10)}, headers=headers)
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]
        elif name == "search":
            r = requests.post("https://api.firecrawl.dev/v1/search", json={"query": arguments["query"]}, headers=headers)
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]
    return [TextContent(type="text", text="Unknown tool")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (rs, ws): await app.run(rs, ws, app.create_initialization_options())

if __name__ == "__main__": import asyncio; asyncio.run(main())
''',
            "requirements.txt": "mcp>=1.0.0 requests",
            "README.md": "# Firecrawl MCP Server - Web scraping with Firecrawl"
        }
    },

    "figma": {
        "description": "Figma design integration",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Figma Integration"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import os, json, requests

app = Server("mcp-figma")
TOKEN = os.environ.get("FIGMA_ACCESS_TOKEN", "")

@app.list_tools()
async def list_tools():
    return [
        Tool(name="get_file", description="Get Figma file",
             inputSchema={"type": "object", "properties": {"file_key": {"type": "string"}}, "required": ["file_key"]}),
        Tool(name="get_styles", description="Get file styles",
             inputSchema={"type": "object", "properties": {"file_key": {"type": "string"}}, "required": ["file_key"]}),
        Tool(name="get_images", description="Export nodes as images",
             inputSchema={"type": "object", "properties": {"file_key": {"type": "string"}, "node_ids": {"type": "array", "items": {"type": "string"}}, "format": {"type": "string", "default": "png"}}, "required": ["file_key", "node_ids"]})
    ]

@app.call_tool()
async def call_tool(name, arguments):
    headers = {"X-Figma-Token": TOKEN}
    base = "https://api.figma.com/v1"
    fk = arguments.get("file_key", "")
    try:
        if name == "get_file":
            r = requests.get(f"{base}/files/{fk}", headers=headers)
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]
        elif name == "get_styles":
            r = requests.get(f"{base}/files/{fk}/styles", headers=headers)
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]
        elif name == "get_images":
            ids = ",".join(arguments.get("node_ids", []))
            r = requests.get(f"{base}/images/{fk}?ids={ids}&format=png", headers=headers)
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]
    return [TextContent(type="text", text="Unknown tool")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (rs, ws): await app.run(rs, ws, app.create_initialization_options())

if __name__ == "__main__": import asyncio; asyncio.run(main())
''',
            "requirements.txt": "mcp>=1.0.0 requests",
            "README.md": "# Figma MCP Server - Figma design integration"
        }
    },

    "postgres": {
        "description": "PostgreSQL database operations",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - PostgreSQL"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import os, json, psycopg2

app = Server("mcp-postgres")
DB_URL = os.environ.get("DATABASE_URL", "")

@app.list_tools()
async def list_tools():
    return [
        Tool(name="query", description="Execute SQL query",
             inputSchema={"type": "object", "properties": {"sql": {"type": "string"}}, "required": ["sql"]}),
        Tool(name="tables", description="List tables",
             inputSchema={"type": "object", "properties": {}}),
        Tool(name="schema", description="Get table schema",
             inputSchema={"type": "object", "properties": {"table": {"type": "string"}}, "required": ["table"]})
    ]

@app.call_tool()
async def call_tool(name, arguments):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        if name == "query":
            cur.execute(arguments["sql"])
            if cur.description:
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
                conn.close()
                return [TextContent(type="text", text=json.dumps({"columns": cols, "rows": rows}, default=str))]
            conn.commit()
            conn.close()
            return [TextContent(type="text", text="OK")]
        elif name == "tables":
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = [r[0] for r in cur.fetchall()]
            conn.close()
            return [TextContent(type="text", text=str(tables))]
        elif name == "schema":
            cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{arguments['table']}'")
            schema = [dict(r) for r in cur.fetchall()]
            conn.close()
            return [TextContent(type="text", text=json.dumps(schema, default=str))]
        conn.close()
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]
    return [TextContent(type="text", text="Unknown tool")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (rs, ws): await app.run(rs, ws, app.create_initialization_options())

if __name__ == "__main__": import asyncio; asyncio.run(main())
''',
            "requirements.txt": "mcp>=1.0.0 psycopg2-binary",
            "README.md": "# PostgreSQL MCP Server - PostgreSQL database operations"
        }
    }
'''

new = old + new_templates + "\n}"

if old in content:
    content = content.replace(old, new)
    with open('generator.py', 'w') as f:
        f.write(content)
    print("Success! Added 3 new templates: firecrawl, figma, postgres")
else:
    print("Pattern not found")
    # Find where the email template ends
    idx = content.find("send_template")
    print(content[idx-20:idx+100] if idx > 0 else "not found")
