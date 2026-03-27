#!/usr/bin/env python3
"""
GitHub Repository Analyzer CLI
Analyzes GitHub repos for trends, issues, and opportunities.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import ssl

# GitHub API configuration
GITHUB_API = "https://api.github.com"

def get_headers():
    return {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Repo-Analyzer/1.0"
    }

def parse_repo(repo_str):
    """Parse 'owner/repo' string."""
    if "/" not in repo_str:
        print(f"Error: Invalid repo format '{repo_str}'. Use 'owner/repo'")
        sys.exit(1)
    return repo_str.split("/")

def fetch_json(url):
    """Fetch JSON from URL with error handling."""
    try:
        req = Request(url, headers=get_headers())
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urlopen(req, context=ctx, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        if e.code == 404:
            print(f"Error: Repository not found")
            sys.exit(1)
        elif e.code == 403:
            print(f"Error: Rate limited. Try again later.")
            sys.exit(1)
        else:
            print(f"Error: HTTP {e.code}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def get_repo_info(owner, repo):
    """Get basic repository info."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}"
    return fetch_json(url)

def get_issues(owner, repo, state="open", limit=30):
    """Get recent issues."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/issues?state={state}&per_page={limit}"
    return fetch_json(url)

def get_stars_history(owner, repo):
    """Get star history via events API."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/events?per_page=100"
    events = fetch_json(url)
    
    star_events = [e for e in events if e.get("type") == "WatchEvent"]
    return len(star_events)

def analyze_repo(owner, repo):
    """Full analysis of a repository."""
    print(f"🔍 Analyzing {owner}/{repo}...\n")
    
    # Get repo info
    info = get_repo_info(owner, repo)
    
    stars = info.get("stargazers_count", 0)
    forks = info.get("forks_count", 0)
    watchers = info.get("watchers_count", 0)
    open_issues = info.get("open_issues_count", 0)
    description = info.get("description", "")
    language = info.get("language", "N/A")
    created = info.get("created_at", "")
    updated = info.get("updated_at", "")
    
    print(f"📊 Basic Info")
    print(f"  Stars:     {stars:,}")
    print(f"  Forks:    {forks:,}")
    print(f"  Watchers: {watchers:,}")
    print(f"  Open Issues: {open_issues:,}")
    print(f"  Language: {language}")
    print(f"  Created:  {created[:10]}")
    print(f"  Updated:  {updated[:10]}")
    print(f"  Desc:     {description[:80]}...")
    print()
    
    # Get open issues
    print(f"📝 Recent Open Issues (top 10)")
    issues = get_issues(owner, repo, "open", 10)
    
    issue_titles = []
    for i, issue in enumerate(issues, 1):
        title = issue.get("title", "")
        labels = [l.get("name", "") for l in issue.get("labels", [])]
        issue_num = issue.get("number", "")
        print(f"  {i}. #{issue_num} {title[:60]}")
        if labels:
            print(f"     Labels: {', '.join(labels[:3])}")
        issue_titles.append(title)
    print()
    
    # Issue analysis
    print(f"🎯 Issue Analysis")
    
    # Common keywords in issues
    keywords = {}
    for title in issue_titles:
        title_lower = title.lower()
        for kw in ["bug", "error", "fail", "crash", "slow", "memory", "redis", 
                   "api", "timeout", "install", "windows", "linux", "mac", 
                   "docker", "docker", "config", "auth", "token"]:
            if kw in title_lower:
                keywords[kw] = keywords.get(kw, 0) + 1
    
    if keywords:
        sorted_kw = sorted(keywords.items(), key=lambda x: -x[1])
        print(f"  Common keywords: {', '.join([f'{k}({v})' for k,v in sorted_kw[:8]])}")
    else:
        print(f"  No common keywords found")
    print()
    
    # Calculate opportunity score
    print(f"💡 Opportunity Score")
    
    # Pain signals
    pain_signals = sum([keywords.get(k, 0) for k in ["bug", "error", "fail", "crash", "slow"]])
    integration_signals = sum([keywords.get(k, 0) for k in ["redis", "api", "install", "docker", "windows", "linux", "mac"]])
    
    print(f"  Pain signals: {pain_signals}")
    print(f"  Integration signals: {integration_signals}")
    
    # Our advantage
    print(f"\n🎯 Differentiation for agent-memory:")
    if integration_signals > 3:
        print(f"  → Focus on easier installation & cross-platform support")
    if pain_signals > 2:
        print(f"  → Focus on stability & fewer bugs")
    if language == "Python":
        print(f"  → Python ecosystem - keep it lightweight")
    
    return {
        "repo": f"{owner}/{repo}",
        "stars": stars,
        "forks": forks,
        "open_issues": open_issues,
        "language": language,
        "pain_signals": pain_signals,
        "integration_signals": integration_signals,
        "keywords": keywords
    }

def main():
    parser = argparse.ArgumentParser(
        description="GitHub Repository Analyzer - Find opportunities in repos"
    )
    parser.add_argument("repo", help="Repository in format 'owner/repo'")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    owner, repo = parse_repo(args.repo)
    result = analyze_repo(owner, repo)
    
    if args.json:
        print("\n" + json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
