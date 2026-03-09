#!/usr/bin/env python3
"""
MCP Server Templates Generator v2
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
                content = f.read(10000)
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
    },
    
    # NEW: GitHub template
    "github": {
        "description": "GitHub API integration (issues, PRs, repos)",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - GitHub Template"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import os

app = Server("mcp-github")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPO", "owner/repo")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_issues",
            description="List repository issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {"type": "string", "description": "open/closed/all"}
                }
            }
        ),
        Tool(
            name="get_issue",
            description="Get a specific issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "number": {"type": "integer", "description": "Issue number"}
                },
                "required": ["number"]
            }
        ),
        Tool(
            name="create_issue",
            description="Create a new issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Issue title"},
                    "body": {"type": "string", "description": "Issue body"}
                },
                "required": ["title"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    url = f"https://api.github.com/repos/{REPO}"
    
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            if name == "list_issues":
                state = arguments.get("state", "open")
                resp = await client.get(f"{url}/issues?state={state}")
                issues = resp.json()
                return [TextContent(type="text", text=str([f"#{i.get('number')}: {i.get('title')}" for i in issues]))]
            
            elif name == "get_issue":
                number = arguments.get("number")
                resp = await client.get(f"{url}/issues/{number}")
                issue = resp.json()
                return [TextContent(type="text", text=f"#{issue.get('number')}: {issue.get('title')}\n\n{issue.get('body')}")]
            
            elif name == "create_issue":
                data = {"title": arguments.get("title"), "body": arguments.get("body", "")}
                resp = await client.post(f"{url}/issues", json=data)
                issue = resp.json()
                return [TextContent(type="text", text=f"Created issue #{issue.get('number')}: {issue.get('title')}")]
        
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
            "README.md": "# GitHub MCP Server\n\n## Usage\n\n```bash\nexport GITHUB_TOKEN=your_token\nexport GITHUB_REPO=owner/repo\npython main.py\n```\n\n## Tools\n\n- `list_issues`: List repository issues\n- `get_issue`: Get issue details\n- `create_issue`: Create new issue\n"
        }
    },
    
    # NEW: Slack template
    "slack": {
        "description": "Slack API integration (channels, messages)",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Slack Template"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import os

app = Server("mcp-slack")

SLACK_TOKEN = os.environ.get("SLACK_TOKEN", "")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_channels",
            description="List Slack channels",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="post_message",
            description="Post a message to a channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "description": "Channel ID"},
                    "text": {"type": "string", "description": "Message text"}
                },
                "required": ["channel", "text"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    url = "https://slack.com/api"
    
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            if name == "list_channels":
                resp = await client.get(f"{url}/conversations.list")
                data = resp.json()
                channels = data.get("channels", [])
                return [TextContent(type="text", text=str([c.get("name") for c in channels]))]
            
            elif name == "post_message":
                data = {"channel": arguments.get("channel"), "text": arguments.get("text")}
                resp = await client.post(f"{url}/chat.postMessage", json=data)
                result = resp.json()
                if result.get("ok"):
                    return [TextContent(type="text", text="Message posted successfully")]
                return [TextContent(type="text", text=f"Error: {result.get('error')}")]
        
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
            "README.md": "# Slack MCP Server\n\n## Usage\n\n```bash\nexport SLACK_TOKEN=xoxb-...\npython main.py\n```\n\n## Tools\n\n- `list_channels`: List Slack channels\n- `post_message`: Post message to channel\n"
        }
    },
    
    # NEW: Notion template
    "notion": {
        "description": "Notion API integration (pages, databases)",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Notion Template"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import os
import json

app = Server("mcp-notion")

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="query_database",
            description="Query a Notion database",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "object", "description": "Filter object"}
                }
            }
        ),
        Tool(
            name="create_page",
            description="Create a new page",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Page title"},
                    "content": {"type": "string", "description": "Page content"}
                },
                "required": ["title"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            if name == "query_database":
                url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
                resp = await client.post(url, json=arguments.get("filter", {}))
                data = resp.json()
                results = data.get("results", [])
                return [TextContent(type="text", text=str([r.get("id") for r in results]))]
            
            elif name == "create_page":
                url = "https://api.notion.com/v1/pages"
                title = arguments.get("title", "Untitled")
                data = {
                    "parent": {"database_id": DATABASE_ID},
                    "properties": {
                        "Name": {"title": [{"text": {"content": title}}]}
                    }
                }
                resp = await client.post(url, json=data)
                page = resp.json()
                return [TextContent(type="text", text=f"Created page: {page.get('id')}")]
        
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
            "README.md": "# Notion MCP Server\n\n## Usage\n\n```bash\nexport NOTION_TOKEN=secret_...\nexport NOTION_DATABASE_ID=...\npython main.py\n```\n\n## Tools\n\n- `query_database`: Query Notion database\n- `create_page`: Create new page\n"
        }
    },
    
    # NEW: Twitter/X template
    "twitter": {
        "description": "Twitter/X API integration (tweets, timeline)",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Twitter/X Template"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import os
import json

app = Server("mcp-twitter")

TWITTER_TOKEN = os.environ.get("TWITTER_TOKEN", "")
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", "")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="post_tweet",
            description="Post a new tweet",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Tweet text"}
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="get_timeline",
            description="Get user timeline",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_results": {"type": "integer", "description": "Max tweets (1-100)"}
                }
            }
        ),
        Tool(
            name="search_tweets",
            description="Search tweets by query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "description": "Max results (10-100)"}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            if name == "post_tweet":
                url = "https://api.twitter.com/2/tweets"
                data = {"text": arguments.get("text", "")}
                resp = await client.post(url, json=data)
                result = resp.json()
                return [TextContent(type="text", text=f"Tweet posted: {result.get('data', {}).get('id')}")]
            
            elif name == "get_timeline":
                url = "https://api.twitter.com/2/users/me/tweets"
                max_results = arguments.get("max_results", 10)
                resp = await client.get(url, params={"max_results": max_results})
                data = resp.json()
                tweets = data.get("data", [])
                return [TextContent(type="text", text=str([t.get("text", "")[:100] for t in tweets]))]
            
            elif name == "search_tweets":
                url = "https://api.twitter.com/2/tweets/search/recent"
                query = arguments.get("query", "")
                max_results = arguments.get("max_results", 10)
                resp = await client.get(url, params={"query": query, "max_results": max_results})
                data = resp.json()
                tweets = data.get("data", [])
                return [TextContent(type="text", text=str([t.get("text", "")[:100] for t in tweets]))]
        
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
            "README.md": "# Twitter/X MCP Server\n\n## Usage\n\n```bash\nexport TWITTER_BEARER_TOKEN=...\npython main.py\n```\n\n## Tools\n\n- `post_tweet`: Post a new tweet\n- `get_timeline`: Get user timeline\n- `search_tweets`: Search tweets by query\n"
        }
    },
    
    # NEW: Email template
    "email": {
        "description": "Email sending via SMTP",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Email Template"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Server("mcp-email")

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", SMTP_USER)

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="send_email",
            description="Send an email",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body (text or HTML)"},
                    "is_html": {"type": "boolean", "description": "Send as HTML"}
                },
                "required": ["to", "subject", "body"]
            }
        ),
        Tool(
            name="send_template",
            description="Send email from template",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email"},
                    "template": {"type": "string", "description": "Template name"},
                    "vars": {"type": "object", "description": "Template variables"}
                },
                "required": ["to", "template"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "send_email":
            to_email = arguments.get("to", "")
            subject = arguments.get("subject", "")
            body = arguments.get("body", "")
            is_html = arguments.get("is_html", False)
            
            msg = MIMEMultipart()
            msg["From"] = FROM_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            
            msg.attach(MIMEText(body, "html" if is_html else "plain"))
            
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
            
            return [TextContent(type="text", text=f"Email sent to {to_email}")]
        
        elif name == "send_template":
            to_email = arguments.get("to", "")
            template_name = arguments.get("template", "")
            vars_dict = arguments.get("vars", {})
            
            templates = {
                "welcome": ("Welcome!", "Welcome {{name}}! Thanks for joining."),
                "reminder": ("Reminder", "Hi {{name}}, this is a reminder for {{event}}."),
                "alert": ("Alert", "Alert: {{message}}")
            }
            
            if template_name not in templates:
                return [TextContent(type="text", text=f"Unknown template: {template_name}")]
            
            subject, body = templates[template_name]
            for key, val in vars_dict.items():
                body = body.replace(f"{{{{{key}}}}}", val)
                subject = subject.replace(f"{{{{{key}}}}}", val)
            
            msg = MIMEMultipart()
            msg["From"] = FROM_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
            
            return [TextContent(type="text", text=f"Template email sent to {to_email}")]
    
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
            "README.md": "# Email MCP Server\n\n## Usage\n\n```bash\nexport SMTP_HOST=smtp.gmail.com\nexport SMTP_PORT=587\nexport SMTP_USER=your@email.com\nexport SMTP_PASS=password\nexport FROM_EMAIL=your@email.com\npython main.py\n```\n\n## Tools\n\n- `send_email`: Send a plain/HTML email\n- `send_template`: Send email from template (welcome, reminder, alert)\n"
        }
    }
    },

    "firecrawl": {
        "description": "Web scraping and crawling with Firecrawl",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Firecrawl Web Scraping Template"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import os, json

app = Server("mcp-firecrawl")
API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="scrape", description="Scrape a web page",
             inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "formats": {"type": "array", "items": {"type": "string"}, "default": ["markdown"]}}, "required": ["url"]}),
        Tool(name="crawl", description="Crawl a website",
             inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "limit": {"type": "integer", "default": 10}}, "required": ["url"]}),
        Tool(name="search", description="Search the web",
             inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]})
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        import requests
        headers = {"Authorization": f"Bearer {API_KEY}"}
        if name == "scrape":
            r = requests.post("https://api.firecrawl.dev/v1/scrape", json={"url": arguments["url"], "formats": arguments.get("formats", ["markdown"])}, headers=headers)
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
            "requirements.txt": "mcp>=1.0.0 requests>=2.31.0",
            "README.md": "# Firecrawl MCP Server\n\n## Usage\nexport FIRECRAWL_API_KEY=your-key\npython main.py\n\n## Tools\n- scrape, crawl, search\n\nGet key at firecrawl.dev"
        }
    },

    "figma": {
        "description": "Figma design integration for AI agents",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""MCP Server - Figma Template"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import os, json

app = Server("mcp-figma")
TOKEN = os.environ.get("FIGMA_ACCESS_TOKEN", "")
FILE_KEY = os.environ.get("FIGMA_FILE_KEY", "")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="get_file", description="Get Figma file data",
             inputSchema={"type": "object", "properties": {"file_key": {"type": "string"}}, "required": ["file_key"]}),
        Tool(name="get_styles", description="Get styles from file",
             inputSchema={"type": "object", "properties": {"file_key": {"type": "string"}}, "required": ["file_key"]}),
        Tool(name="get_images", description="Export nodes as images",
             inputSchema={"type": "object", "properties": {"file_key": {"type": "string"}, "node_ids": {"type": "array", "items": {"type": "string"}}, "format": {"type": "string", "default": "png"}}, "required": ["file_key", "node_ids"]})
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        import requests
        headers = {"X-Figma-Token": TOKEN}
        base = "https://api.figma.com/v1"
        fk = arguments.get("file_key", FILE_KEY)
        if name == "get_file":
            r = requests.get(f"{base}/files/{fk}", headers=headers)
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]
        elif name == "get_styles":
            r = requests.get(f"{base}/files/{fk}/styles", headers=headers)
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]
        elif name == "get_images":
            ids = ",".join(arguments.get("node_ids", []))
            fmt = arguments.get("format", "png")
            r = requests.get(f"{base}/images/{fk}?ids={ids}&format={fmt}", headers=headers)
            return [TextContent(type="text", text=json.dumps(r.json(), indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]
    return [TextContent(type="text", text="Unknown tool")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (rs, ws): await app.run(rs, ws, app.create_initialization_options())

if __name__ == "__main__": import asyncio; asyncio.run(main())
''',
            "requirements.txt": "mcp>=1.0.0 requests>=2.31.0",
            "README.md": "# Figma MCP Server\n\n## Usage\nexport FIGMA_ACCESS_TOKEN=your-token\nexport FFIGMA_FILE_KEY=file-key\npython main.py\n\nGet token from Figma Settings > Account"
        }
    }
}
def create_project(name: str, template: str):
    """Create a new MCP server project."""
    if template not in TEMPLATES:
        print(f"Error: Unknown template '{template}'")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)
    
    os.makedirs(name, exist_ok=True)
    
    for filename, content in TEMPLATES[template]["files"].items():
        filepath = os.path.join(name, filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Created: {filename}")
    
    print(f"\nDone! Run:\n  cd {name} && pip install -r requirements.txt")


def list_templates():
    """List available templates."""
    return list(TEMPLATES.keys())


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Server Templates v2")
    subparsers = parser.add_subparsers()
    
    new_parser = subparsers.add_parser("new", help="Create new MCP server")
    new_parser.add_argument("name", help="Project name")
    new_parser.add_argument("--template", "-t", default="database",
                           choices=list(TEMPLATES.keys()),
                           help="Template to use")
    
    subparsers.add_parser("list", help="List available templates")
    
    args = parser.parse_args()
    
    if hasattr(args, 'list') and args.list:
        list_templates()
    elif hasattr(args, 'name'):
        create_project(args.name, args.template)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
