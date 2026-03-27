#!/usr/bin/env python3
"""
MCP Template Generator - Generate MCP server templates
"""

import argparse
import os

TEMPLATES = {
    "basic": {
        "name": "basic-mcp-server",
        "description": "Basic MCP server with read/write tools",
        "files": {
            "server.py": '''#!/usr/bin/env python3
"""Basic MCP Server"""
from modelcontextprotocol import Server

class BasicServer(Server):
    def __init__(self):
        super().__init__("basic-mcp-server", "1.0.0")
        
    def handle_request(self, method, params):
        if method == "tools/list":
            return {
                "tools": [
                    {"name": "echo", "description": "Echo back the input"}
                ]
            }
        return None

if __name__ == "__main__":
    server = BasicServer()
    server.run()
'''
        }
    },
    "memory": {
        "name": "memory-mcp-server",
        "description": "MCP server for agent-memory",
        "files": {
            "server.py": '''#!/usr/bin/env python3
"""Memory MCP Server"""
from modelcontextprotocol import Server

class MemoryServer(Server):
    def __init__(self):
        super().__init__("memory-mcp-server", "1.0.0")
        self.memories = {}
        
    def handle_request(self, method, params):
        if method == "tools/list":
            return {
                "tools": [
                    {"name": "memory_add", "description": "Add a memory"},
                    {"name": "memory_search", "description": "Search memories"},
                    {"name": "memory_get", "description": "Get a memory by ID"}
                ]
            }
        return None

if __name__ == "__main__":
    server = MemoryServer()
    server.run()
'''
        }
    }
}

def generate(template, output_dir):
    """Generate a template."""
    if template not in TEMPLATES:
        print(f"Unknown template: {template}")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        return
    
    t = TEMPLATES[template]
    name = t["name"]
    target = os.path.join(output_dir, name)
    
    os.makedirs(target, exist_ok=True)
    
    for filename, content in t["files"].items():
        path = os.path.join(target, filename)
        with open(path, "w") as f:
            f.write(content)
        print(f"Created: {path}")
    
    # Create README
    readme = f"# {name}\n\n{t['description']}\n"
    with open(os.path.join(target, "README.md"), "w") as f:
        f.write(readme)
    
    print(f"\n✅ Generated {name} in {target}")

def main():
    parser = argparse.ArgumentParser(description="MCP Template Generator")
    parser.add_argument("template", nargs="?", default="basic", help="Template name")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    
    args = parser.parse_args()
    generate(args.template, args.output)

if __name__ == "__main__":
    main()