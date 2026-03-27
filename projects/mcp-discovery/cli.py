#!/usr/bin/env python3
"""
MCP Server Discovery CLI
Discover and analyze MCP servers from the ecosystem.
"""

import argparse
import json
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import ssl
import re

# Smithery registry API
SMITHERY_API = "https://smithery.ai/api/mcp"

def fetch_json(url):
    """Fetch JSON from URL."""
    try:
        req = Request(url, headers={"User-Agent": "MCP-Discovery/1.0"})
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urlopen(req, context=ctx, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": str(e)}

def search_npm(keyword):
    """Search npm for MCP servers."""
    url = f"https://registry.npmjs.org/-/v1/search?text={keyword}&size=20"
    return fetch_json(url)

def get_npm_package(name):
    """Get npm package details."""
    url = f"https://registry.npmjs.org/{name}/latest"
    return fetch_json(url)

def analyze_mcp_server(name):
    """Analyze a single MCP server."""
    print(f"🔍 Analyzing {name}...")
    
    pkg = get_npm_package(name)
    
    if "error" in pkg:
        print(f"❌ Error: {pkg['error']}")
        return None
    
    version = pkg.get("version", "N/A")
    description = pkg.get("description", "")
    keywords = pkg.get("keywords", [])
    repo = pkg.get("repository", {})
    
    if isinstance(repo, dict):
        repo_url = repo.get("url", "")
    else:
        repo_url = str(repo)
    
    # Clean repo URL
    if repo_url.startswith("git+"):
        repo_url = repo_url[4:]
    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]
    
    print(f"📦 {name} v{version}")
    print(f"   {description[:80] if description else 'No description'}")
    print(f"   Keywords: {', '.join(keywords[:5]) if keywords else 'None'}")
    print(f"   Repo: {repo_url[:60] if repo_url else 'None'}")
    
    return {
        "name": name,
        "version": version,
        "description": description,
        "keywords": keywords,
        "repo": repo_url
    }

def main():
    parser = argparse.ArgumentParser(
        description="MCP Server Discovery - Find MCP servers on npm"
    )
    parser.add_argument("search", nargs="?", default="mcp-server", help="Search keyword")
    parser.add_argument("--analyze", help="Analyze specific package")
    
    args = parser.parse_args()
    
    if args.analyze:
        analyze_mcp_server(args.analyze)
        return
    
    print(f"🔍 Searching npm for '{args.search}'...\n")
    
    results = search_npm(args.search)
    
    if "objects" not in results:
        print("❌ No results found")
        return
    
    packages = results["objects"][:15]
    
    print(f"📦 Found {len(packages)} packages:\n")
    
    for i, pkg in enumerate(packages, 1):
        pkg_info = pkg.get("package", {})
        name = pkg_info.get("name", "")
        desc = pkg_info.get("description", "")
        version = pkg_info.get("version", "")
        
        print(f"{i}. {name} ({version})")
        print(f"   {desc[:70] if desc else 'No description'}...")
        print()

if __name__ == "__main__":
    main()
