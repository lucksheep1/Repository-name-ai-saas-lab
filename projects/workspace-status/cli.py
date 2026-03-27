#!/usr/bin/env python3
"""
Workspace Status - Show workspace status
"""

import subprocess
import os
from pathlib import Path

def get_git_status():
    """Get git status."""
    root = "/root/.openclaw/workspace"
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def get_commit_history(count=5):
    """Get recent commits."""
    root = "/root/.openclaw/workspace"
    result = subprocess.run(
        ["git", "log", f"-{count}", "--oneline"],
        cwd=root,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def count_projects():
    """Count projects."""
    root = Path("/root/.openclaw/workspace/projects")
    return len([d for d in root.iterdir() if d.is_dir() and (d / "README.md").exists()])

def main():
    print("📊 Workspace Status\n")
    
    # Git
    status = get_git_status()
    if status:
        print(f"🔄 Git: {len(status.split(chr(10)))} changes pending")
    else:
        print("✅ Git: Clean")
    
    # Commits
    commits = get_commit_history(5)
    print(f"\n📝 Recent commits:")
    for line in commits.split("\n"):
        print(f"   {line}")
    
    # Projects
    n = count_projects()
    print(f"\n📦 Projects: {n}")
    
    # OpenClaw
    print(f"\n🤖 OpenClaw: Running")

if __name__ == "__main__":
    main()