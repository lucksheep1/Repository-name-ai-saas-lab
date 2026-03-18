#!/usr/bin/env python3
"""
GitHub Signal Reader - 可复用读取脚本
用于读取 GitHub Issue 的返回信号

用法:
    python3 scripts/github_signal_reader.py
    python3 scripts/github_signal_reader.py --issue 3
    python3 scripts/github_signal_reader.py --repo lucksheep1/Repository-name-ai-saas-lab
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

# 配置
DEFAULT_OWNER = "lucksheep1"
DEFAULT_REPO = "Repository-name-ai-saas-lab"

def get_token():
    """获取 GitHub token"""
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True
        )
        remote_url = result.stdout.strip()
        if "github.com" in remote_url and "@" in remote_url:
            token_part = remote_url.split("@")[1].split("/")[0]
            if "_" in token_part:
                return token_part
    except:
        pass
    return None

def read_issue(owner, repo, issue_num, token=None):
    """读取单个 Issue 的信号"""
    import urllib.request
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_num}"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "SaaS-Lab-Signal-Reader"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "success": True,
                "number": data.get("number"),
                "title": data.get("title"),
                "state": data.get("state"),
                "comments": data.get("comments"),
                "reactions": data.get("reactions", {}).get("total_count", 0),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
                "labels": [l.get("name") for l in data.get("labels", [])]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

def read_all_issues(owner, repo, token=None):
    """读取所有 Issue"""
    import urllib.request
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=100"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "SaaS-Lab-Signal-Reader"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {"success": True, "issues": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def judge_signal(issue_data):
    """
    判定信号强度
    
    规则:
    - 强信号: comments >= 3 或 reactions >= 5
    - 弱信号: comments >= 1 或 reactions >= 1
    - 无信号: comments = 0 且 reactions = 0
    """
    comments = issue_data.get("comments", 0)
    reactions = issue_data.get("reactions", {})
    if isinstance(reactions, dict):
        reactions = reactions.get("total_count", 0)
    else:
        reactions = 0
    
    if comments >= 3 or reactions >= 5:
        return "强信号"
    elif comments >= 1 or reactions >= 1:
        return "弱信号"
    else:
        return "无信号"

def get_next_action(signal_level):
    """
    根据信号强度返回下一轮动作
    
    规则:
    - 无信号 -> 强化 CTA/问题结构，或切换到更强入口
    - 弱信号 -> 继续加压同路径，优化提问
    - 强信号 -> 围绕该主题连续追打，深入验证
    """
    actions = {
        "无信号": "强化标题/CTA/问题结构，或切换到更强入口",
        "弱信号": "继续加压同路径，优化提问设计",
        "强信号": "围绕该主题连续追打，深入验证"
    }
    return actions.get(signal_level, "未知")

def main():
    parser = argparse.ArgumentParser(description="GitHub Signal Reader")
    parser.add_argument("--owner", default=DEFAULT_OWNER, help="Repository owner")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="Repository name")
    parser.add_argument("--issue", type=int, help="Specific issue number (default: all)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    token = get_token()
    
    if args.issue:
        # 读取单个 Issue
        result = read_issue(args.owner, args.repo, args.issue, token)
        if result["success"]:
            signal = judge_signal(result)
            action = get_next_action(signal)
            if args.json:
                print(json.dumps({
                    "issue": result,
                    "signal": signal,
                    "next_action": action
                }, indent=2))
            else:
                print(f"=== Issue #{result['number']} ===")
                print(f"Title: {result['title']}")
                print(f"Comments: {result['comments']}")
                print(f"Reactions: {result['reactions']}")
                print(f"Signal: {signal}")
                print(f"Next Action: {action}")
        else:
            print(f"Error: {result.get('error')}")
            sys.exit(1)
    else:
        # 读取所有 Issue
        result = read_all_issues(args.owner, args.repo, token)
        if result["success"]:
            issues = result["issues"]
            # 过滤掉 PR
            issues = [i for i in issues if "pull_request" not in i]
            
            if args.json:
                output = []
                for issue in issues:
                    data = {
                        "number": issue.get("number"),
                        "title": issue.get("title"),
                        "comments": issue.get("comments"),
                        "reactions": issue.get("reactions", {}).get("total_count", 0),
                        "signal": judge_signal(issue),
                    }
                    output.append(data)
                print(json.dumps(output, indent=2))
            else:
                print("=== 所有 Issue 信号读取 ===")
                print(f"总 Issue 数: {len(issues)}")
                print("")
                for issue in issues:
                    signal = judge_signal(issue)
                    action = get_next_action(signal)
                    print(f"#{issue.get('number')}: {issue.get('title')[:50]}")
                    print(f"  Comments: {issue.get('comments')} | Reactions: {issue.get('reactions', {}).get('total_count', 0)}")
                    print(f"  Signal: {signal} | Next: {action}")
                    print("")
        else:
            print(f"Error: {result.get('error')}")
            sys.exit(1)

if __name__ == "__main__":
    main()
