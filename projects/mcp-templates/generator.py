#!/usr/bin/env python3
"""
MCP Server Templates Generator
Quick-start templates for Model Context Protocol servers.
"""
import os
import sys
import shutil
from pathlib import Path


TEMPLATES = {
    "database": {
        "description": "Simple SQLite database query tool",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Database Template"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import sqlite3
import os

app = Server("mcp-database")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="query",
            description="Execute a SQL query on the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL query"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="tables",
            description="List all tables in the database",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    db_path = os.environ.get("DB_PATH", "data.db")
    
    if name == "query":
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(arguments["query"])
            if arguments["query"].strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                conn.close()
                return [TextContent(type="text", text=str(results))]
            else:
                conn.commit()
                conn.close()
                return [TextContent(type="text", text="OK")]
        except Exception as e:
            conn.close()
            return [TextContent(type="text", text=f"Error: {e}")]
    
    elif name == "tables":
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        return [TextContent(type="text", text=str([t[0] for t in tables]))]
    
    return [TextContent(type="text", text="Unknown tool")]

async def main():
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
''',
            "requirements.txt": "mcp>=1.0.0",
            "README.md": "# Database MCP Server\n\n## Usage\n\n```bash\nexport DB_PATH=my.db\npython main.py\n```\n\n## Tools\n\n- `query`: Execute SQL queries\n- `tables`: List all tables\n"
        }
    },
    "api": {
        "description": "REST API integration",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - API Template"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import os

app = Server("mcp-api")

BASE_URL = os.environ.get("API_BASE_URL", "https://api.example.com")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get",
            description="Make a GET request",
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {"type": "string", "description": "API endpoint"},
                    "params": {"type": "object", "description": "Query params"}
                },
                "required": ["endpoint"]
            }
        ),
        Tool(
            name="post",
            description="Make a POST request",
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {"type": "string", "description": "API endpoint"},
                    "data": {"type": "object", "description": "Request body"}
                },
                "required": ["endpoint"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    endpoint = arguments.get("endpoint", "")
    url = f"{BASE_URL}/{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            if name == "get":
                params = arguments.get("params", {})
                resp = await client.get(url, params=params)
                return [TextContent(type="text", text=resp.text)]
            
            elif name == "post":
                data = arguments.get("data", {})
                resp = await client.post(url, json=data)
                return [TextContent(type="text", text=resp.text)]
            
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
    
    return [TextContent(type="text", text="Unknown tool")]

async def main():
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
''',
            "requirements.txt": "mcp>=1.0.0 httpx",
            "README.md": "# API MCP Server\n\n## Usage\n\n```bash\nexport API_BASE_URL=https://api.example.com\npython main.py\n```\n\n## Tools\n\n- `get`: Make GET requests\n- `post`: Make POST requests\n"
        }
    },
    "filesystem": {
        "description": "File system operations",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Filesystem Template"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import os
from pathlib import Path

app = Server("mcp-filesystem")

ROOT_DIR = os.environ.get("ROOT_DIR", ".")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="read",
            description="Read a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"}
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="list",
            description="List directory contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path"}
                },
                "required": ["path"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    path = arguments.get("path", "")
    full_path = os.path.join(ROOT_DIR, path)
    
    # Security: prevent directory traversal
    if ".." in path:
        return [TextContent(type="text", text="Error: Invalid path")]
    
    try:
        if name == "read":
            with open(full_path, "r") as f:
                content = f.read(10000)  # Limit to 10KB
                return [TextContent(type="text", text=content)]
        
        elif name == "list":
            items = os.listdir(full_path)
            return [TextContent(type="text", text=str(items))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]
    
    return [TextContent(type="text", text="Unknown tool")]

async def main():
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
''',
            "requirements.txt": "mcp>=1.0.0",
            "README.md": "# Filesystem MCP Server\n\n## Usage\n\n```bash\nexport ROOT_DIR=/path/to/dir\npython main.py\n```\n\n## Tools\n\n- `read`: Read a file\n- `list`: List directory contents\n"
        }
    }
}


def create_project(name: str, template: str):
    """Create a new MCP server project."""
    if template not in TEMPLATES:
        print(f"Error: Unknown template '{template}'")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)
    
    # Create directory
    os.makedirs(name, exist_ok=True)
    
    # Generate files
    for filename, content in TEMPLATES[template]["files"].items():
        filepath = os.path.join(name, filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Created: {filename}")
    
    print(f"\nDone! Run:\n  cd {name} && pip install -r requirements.txt")


def list_templates():
    """List available templates."""
    print("Available templates:")
    for name, info in TEMPLATES.items():
        print(f"  {name}: {info['description']}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Server Templates")
    subparsers = parser.add_subparsers()
    
    # new command
    new_parser = subparsers.add_parser("new", help="Create new MCP server")
    new_parser.add_argument("name", help="Project name")
    new_parser.add_argument("--template", "-t", default="database",
                           choices=list(TEMPLATES.keys()),
                           help="Template to use")
    
    # list command
    subparsers.add_parser("list", help="List available templates")
    
    args = parser.parse_args()
    
    if "list" in args and args.list:
        list_templates()
    elif "name" in args:
        create_project(args.name, args.template)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
