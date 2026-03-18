#!/usr/bin/env python3
"""
GitHub Issue Creator - 可复用脚本
用于自动化创建 GitHub Issue

用法:
    python3 scripts/github_issue.py --title "Title" --body "Body"
    python3 scripts/github_issue.py --title "Title" --body "Body" --label bug
"""

import argparse
import json
import os
import subprocess
import sys

# 默认配置
DEFAULT_OWNER = "lucksheep1"
DEFAULT_REPO = "Repository-name-ai-saas-lab"
DEFAULT_TOKEN_ENV = "GITHUB_TOKEN"

def get_token():
    """从环境变量或配置文件获取 token"""
    token = os.environ.get(DEFAULT_TOKEN_ENV)
    if token:
        return token
    
    # 尝试从 git remote 获取
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True
        )
        remote_url = result.stdout.strip()
        if "github.com" in remote_url and "@" in remote_url:
            # 提取 token from git remote URL
            token_part = remote_url.split("@")[1].split("/")[0]
            if "_" in token_part:
                return token_part
    except:
        pass
    
    raise ValueError(f"GitHub token not found. Set {DEFAULT_TOKEN_ENV} or use git remote with embedded token.")

def create_issue(owner, repo, title, body, labels=None):
    """创建 GitHub Issue"""
    import urllib.request
    import urllib.error
    
    token = get_token()
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    data = {
        "title": title,
        "body": body
    }
    if labels:
        data["labels"] = labels
    
    json_data = json.dumps(data).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SaaS-Lab-GitHub-Issue-Creator"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return {
                "success": True,
                "url": result.get("html_url"),
                "number": result.get("number"),
                "id": result.get("id")
            }
    except urllib.error.HTTPError as e:
        error_body = json.loads(e.read().decode("utf-8"))
        return {
            "success": False,
            "error": error_body.get("message"),
            "docs": error_body.get("documentation_url")
        }

def main():
    parser = argparse.ArgumentParser(description="GitHub Issue Creator")
    parser.add_argument("--title", required=True, help="Issue title")
    parser.add_argument("--body", required=True, help="Issue body (markdown)")
    parser.add_argument("--owner", default=DEFAULT_OWNER, help="Repository owner")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="Repository name")
    parser.add_argument("--label", help="Comma-separated labels")
    
    args = parser.parse_args()
    
    labels = args.label.split(",") if args.label else None
    
    result = create_issue(args.owner, args.repo, args.title, args.body, labels)
    
    if result["success"]:
        print(f"✓ Issue created successfully!")
        print(f"  URL: {result['url']}")
        print(f"  Number: {result['number']}")
        sys.exit(0)
    else:
        print(f"✗ Failed to create issue: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
