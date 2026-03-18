#!/usr/bin/env python3
"""
GitHub Signal Reader - Enhanced Version
增强版信号读取脚本 - 支持定时检查和自动提醒

用法:
    python3 scripts/github_signal_reader.py              # 读取所有 Issue
    python3 scripts/github_signal_reader.py --issue 3   # 读取特定 Issue
    python3 scripts/github_signal_reader.py --check     # 定时检查模式
    python3 scripts/github_signal_reader.py --json       # JSON 输出
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime

# 配置
DEFAULT_OWNER = "lucksheep1"
DEFAULT_REPO = "Repository-name-ai-saas-lab"
CHECK_INTERVAL = 300  # 5分钟检查一次

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
            comments = data.get("comments", 0)
            reactions = data.get("reactions", {})
            if isinstance(reactions, dict):
                reactions = reactions.get("total_count", 0)
            return {
                "success": True,
                "number": data.get("number"),
                "title": data.get("title"),
                "state": data.get("state"),
                "comments": comments,
                "reactions": reactions,
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
            issues = [i for i in data if "pull_request" not in i]
            return {"success": True, "issues": issues}
    except Exception as e:
        return {"success": False, "error": str(e)}

def judge_signal(comments, reactions):
    """判定信号强度"""
    if comments >= 3 or reactions >= 5:
        return "强信号"
    elif comments >= 1 or reactions >= 1:
        return "弱信号"
    else:
        return "无信号"

def get_next_action(signal_level):
    """根据信号强度返回下一轮动作"""
    actions = {
        "无信号": "强化标题/CTA/问题结构，或切换到更强入口",
        "弱信号": "继续加压同路径，优化提问设计",
        "强信号": "围绕该主题连续追打，深入验证"
    }
    return actions.get(signal_level, "未知")

def check_continuously(owner, repo, token, interval=CHECK_INTERVAL):
    """持续检查模式"""
    print(f"=== 持续检查模式启动 ===")
    print(f"检查间隔: {interval}秒")
    print(f"仓库: {owner}/{repo}")
    print(f"按 Ctrl+C 停止")
    print("")
    
    previous_state = {}
    
    while True:
        result = read_all_issues(owner, repo, token)
        if result["success"]:
            signal_issues = []
            for issue in result["issues"]:
                num = issue.get("number")
                comments = issue.get("comments", 0)
                reactions = issue.get("reactions", {})
                if isinstance(reactions, dict):
                    reactions = reactions.get("total_count", 0)
                signal = judge_signal(comments, reactions)
                
                # 检查变化
                prev = previous_state.get(num, {})
                prev_comments = prev.get("comments", -1)
                prev_reactions = prev.get("reactions", -1)
                
                changed = ""
                if prev_comments != comments:
                    changed += f"📬评论:{prev_comments}→{comments} "
                if prev_reactions != reactions:
                    changed += f"👍表情:{prev_reactions}→{reactions} "
                
                signal_issues.append({
                    "number": num,
                    "title": issue.get("title", "")[:40],
                    "comments": comments,
                    "reactions": reactions,
                    "signal": signal,
                    "changed": changed
                })
                
                previous_state[num] = {"comments": comments, "reactions": reactions}
            
            # 排序：按信号强度
            signal_issues.sort(key=lambda x: (
                0 if x["signal"] == "强信号" else 1 if x["signal"] == "弱信号" else 2
            ))
            
            # 输出
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ", end="")
            
            # 检查是否有新信号
            has_new = any(s.get("changed") for s in signal_issues)
            if has_new:
                print("🔔 有新变化!")
                for s in signal_issues:
                    if s.get("changed"):
                        print(f"  #{s['number']}: {s['changed']}")
            else:
                print("⏳ 暂无新信号")
                
            # 显示信号统计
            stats = {"强信号": 0, "弱信号": 0, "无信号": 0}
            for s in signal_issues:
                stats[s["signal"]] += 1
            print(f"  统计: {' '.join([f'{k}:{v}' for k,v in stats.items() if v > 0])}")
        
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="GitHub Signal Reader - Enhanced")
    parser.add_argument("--owner", default=DEFAULT_OWNER, help="Repository owner")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="Repository name")
    parser.add_argument("--issue", type=int, help="Specific issue number")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--check", action="store_true", help="Continuous check mode")
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL, help="Check interval in seconds")
    
    args = parser.parse_args()
    
    token = get_token()
    
    if args.check:
        check_continuously(args.owner, args.repo, token, args.interval)
        return
    
    if args.issue:
        result = read_issue(args.owner, args.repo, args.issue, token)
        if result["success"]:
            signal = judge_signal(result["comments"], result["reactions"])
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
        result = read_all_issues(args.owner, args.repo, token)
        if result["success"]:
            issues = result["issues"]
            
            if args.json:
                output = []
                for issue in issues:
                    comments = issue.get("comments", 0)
                    reactions = issue.get("reactions", {})
                    if isinstance(reactions, dict):
                        reactions = reactions.get("total_count", 0)
                    data = {
                        "number": issue.get("number"),
                        "title": issue.get("title"),
                        "comments": comments,
                        "reactions": reactions,
                        "signal": judge_signal(comments, reactions),
                    }
                    output.append(data)
                print(json.dumps(output, indent=2))
            else:
                print("=== 所有 Issue 信号读取 ===")
                print(f"总 Issue 数: {len(issues)}")
                print("")
                for issue in issues:
                    comments = issue.get("comments", 0)
                    reactions = issue.get("reactions", {})
                    if isinstance(reactions, dict):
                        reactions = reactions.get("total_count", 0)
                    signal = judge_signal(comments, reactions)
                    action = get_next_action(signal)
                    print(f"#{issue.get('number')}: {issue.get('title', '')[:50]}")
                    print(f"  Comments: {comments} | Reactions: {reactions}")
                    print(f"  Signal: {signal} | Next: {action}")
                    print("")
        else:
            print(f"Error: {result.get('error')}")
            sys.exit(1)

if __name__ == "__main__":
    main()
