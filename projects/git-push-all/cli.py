#!/usr/bin/env python3
"""
Git Push All - Push all project repos
"""

import argparse
import os
import subprocess
from pathlib import Path

def find_git_repos(root):
    """Find all git repositories."""
    repos = []
    for d in Path(root).iterdir():
        if d.is_dir() and (d / ".git").exists():
            repos.append(d)
    return repos

def push_repo(repo_path, dry_run=False):
    """Push a single repo."""
    name = repo_path.name
    try:
        # Check if there are changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if not result.stdout.strip():
            print(f"⏭️  {name}: No changes")
            return True
        
        # Check remote
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"⏭️  {name}: No remote")
            return True
        
        if dry_run:
            print(f"🔄 {name}: Would push")
            return True
        
        # Push
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {name}: Pushed")
            return True
        else:
            print(f"❌ {name}: {result.stderr[:50]}")
            return False
    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Git Push All")
    parser.add_argument("path", nargs="?", default="projects", help="Root directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be pushed")
    
    args = parser.parse_args()
    
    repos = find_git_repos(args.path)
    print(f"📦 Found {len(repos)} git repos\n")
    
    success = 0
    for repo in repos:
        if push_repo(repo, args.dry_run):
            success += 1
    
    print(f"\n✅ {success}/{len(repos)} repos")

if __name__ == "__main__":
    main()