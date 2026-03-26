#!/usr/bin/env python3
"""
git-memory: Ask questions about your git history in natural language.

Uses agent-memory to store git context, enabling smarter Q&A about
your repository's history, patterns, and changes.

Usage:
    python git_memory.py ask "what did we change last Tuesday?"
    python git_memory.py log --limit 10
    python git_memory.py add-context "important refactoring in commit abc123"
    python git_memory.py stats
"""

import argparse
import subprocess
import sys
import json
import os
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))
from agent_memory import Memory


def run(cmd, capture=True):
    """Run a shell command, return stdout."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=capture,
            text=True, cwd=os.getcwd()
        )
        return result.stdout.strip() if capture else ""
    except Exception as e:
        return f"[error] {e}"


def get_git_log(limit=50):
    """Get recent git log as structured data."""
    fmt = "%H|%ai|%an|%s"
    out = run(f'git log --format="{fmt}" -n {limit}')
    commits = []
    for line in out.split("\n"):
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 4:
                commits.append({
                    "hash": parts[0],
                    "date": parts[1],
                    "author": parts[2],
                    "message": "|".join(parts[3:]),
                })
    return commits


def get_commits_by_date(start_date, end_date=None):
    """Get commits within a date range."""
    end = end_date or datetime.now().strftime("%Y-%m-%d")
    out = run(
        f'git log --since="{start_date}" --until="{end}" '
        f'--format="%H|%ai|%an|%s" -n 200'
    )
    commits = []
    for line in out.split("\n"):
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 4:
                commits.append({
                    "hash": parts[0],
                    "date": parts[1],
                    "author": parts[2],
                    "message": "|".join(parts[3:]),
                })
    return commits


def get_changed_files(commit_hash):
    """Get files changed in a commit."""
    out = run(f'git show --name-only --format="" {commit_hash}')
    return [f for f in out.split("\n") if f.strip()]


def analyze_impact(commit_hash):
    """Analyze impact of a commit: files changed, lines added/removed."""
    out = run(f'git show --stat --format="" {commit_hash}')
    lines = out.strip().split("\n")
    files = sum(1 for l in lines if "|" in l)
    return files, out.strip()


def get_diff_summary(commit_hash):
    """Get diff summary for a commit."""
    return run(f'git show --format="%B" --stat {commit_hash}')


def cmd_ask(memory: Memory, question: str):
    """Answer a question about git history using memory context."""
    print(f"\n🔍 Question: {question}\n")

    q_lower = question.lower()

    # Parse time references
    days_refs = {
        "today": 0, "yesterday": 1, "last monday": 7,
        "last week": 7, "this week": 7, "last tuesday": 14,
        "two days": 2, "three days": 3, "week": 7,
    }
    days_ago = None
    for ref, days in days_refs.items():
        if ref in q_lower:
            days_ago = days
            break
    # Try to parse "N days ago"
    import re
    m = re.search(r"(\d+)\s+days?\s+ago", q_lower)
    if m:
        days_ago = int(m.group(1))

    # Time range queries
    if "last week" in q_lower or "this week" in q_lower or days_ago == 7:
        commits = get_commits_by_date(
            (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        )
        print(f"📅 Found {len(commits)} commits from the last 7 days:\n")
        for c in commits[:10]:
            print(f"  [{c['hash'][:7]}] {c['date'][:10]} {c['author']}")
            print(f"      {c['message']}")
            print()

    elif "last tuesday" in q_lower or days_ago == 14:
        # Find last Tuesday
        today = datetime.now()
        tuesday = today - timedelta(days=(today.weekday() - 1) % 7 + (7 if today.weekday() == 0 else 0))
        if "last tuesday" in q_lower:
            tuesday = tuesday - timedelta(days=7)
        commits = get_commits_by_date(
            tuesday.strftime("%Y-%m-%d"),
            (tuesday + timedelta(days=1)).strftime("%Y-%m-%d")
        )
        print(f"📅 Found {len(commits)} commits on {tuesday.strftime('%Y-%m-%d')}:\n")
        for c in commits:
            print(f"  [{c['hash'][:7]}] {c['author']}: {c['message']}")
        print()

    elif days_ago is not None:
        start = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        commits = get_commits_by_date(start)
        print(f"📅 Found {len(commits)} commits in last {days_ago} days:\n")
        for c in commits[:10]:
            print(f"  [{c['hash'][:7]}] {c['date'][:10]} {c['author']}: {c['message']}")
        print()

    # Author queries
    elif any(w in q_lower for w in ["who", "author", "by"]):
        if "most" in q_lower or "top" in q_lower:
            out = run("git shortlog -sn | head -5")
            print("👥 Top contributors:\n")
            for line in out.split("\n")[:5]:
                if line.strip():
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        print(f"  {parts[0]} commits — {parts[1]}")
        else:
            print("Use: git-memory ask 'who made the most commits?'")

    # File queries
    elif "file" in q_lower or "change" in q_lower:
        if "recent" in q_lower or "last" in q_lower:
            commits = get_git_log(20)
            all_files = {}
            for c in commits:
                files = get_changed_files(c["hash"])
                for f in files:
                    all_files[f] = all_files.get(f, 0) + 1
            sorted_files = sorted(all_files.items(), key=lambda x: x[1], reverse=True)
            print("📁 Most frequently changed files (recent 20 commits):\n")
            for f, count in sorted_files[:10]:
                print(f"  {count}x  {f}")
        else:
            print("Use: git-memory ask 'what files changed recently?'")

    # Pattern queries
    elif "pattern" in q_lower or "trend" in q_lower:
        commits = get_git_log(50)
        print(f"📊 Commit activity (last {len(commits)} commits):\n")
        dates = {}
        for c in commits:
            d = c["date"][:10]
            dates[d] = dates.get(d, 0) + 1
        for date, count in sorted(dates.items()):
            bar = "█" * count
            print(f"  {date}  {bar} ({count})")
        print()

    # Bug/fix queries
    elif "fix" in q_lower or "bug" in q_lower or "patch" in q_lower:
        out = run(r'git log --grep="fix\|bug\|patch" --format="%H|%s" -n 20')
        fixes = [l.split("|", 1) for l in out.split("\n") if "|" in l]
        print(f"🐛 Found {len(fixes)} commits mentioning fix/bug/patch:\n")
        for h, msg in fixes[:10]:
            print(f"  [{h[:7]}] {msg}")
        print()

    # Default
    else:
        # General recent activity
        commits = get_git_log(10)
        print(f"📜 Recent commits:\n")
        for c in commits:
            print(f"  [{c['hash'][:7]}] {c['date'][:10]} {c['author']}")
            print(f"      {c['message']}")
            print()

    # Check memory for context
    context_results = memory.search(question)
    if context_results:
        print(f"💡 Context from memory ({len(context_results)} results):\n")
        for r in context_results[:3]:
            text = r.get("text", "")[:200]
            print(f"  → {text}")
            print()


def cmd_log(args, memory: Memory):
    """Show recent git log."""
    commits = get_git_log(args.limit)
    print(f"\n📜 Last {len(commits)} commits:\n")
    for c in commits:
        print(f"[{c['hash'][:7]}] {c['date'][:10]} {c['author']}")
        print(f"    {c['message']}")
        print()


def cmd_stats(args, memory: Memory):
    """Show git statistics."""
    total = run("git rev-list --count HEAD")
    branches = run("git branch | wc -l")
    contributors = run("git shortlog -sn | wc -l")
    active = run(
        "git log --since='90 days ago' --format='%an' | sort -u | wc -l"
    )

    print(f"""
📊 Git Stats
─────────────────────────────────────
  Total commits:  {total}
  Branches:       {branches}
  Contributors:   {contributors}
  Active (90d):   {active}

  Last commit:    {get_git_log(1)[0]['date'][:10]}
  Last message:   {get_git_log(1)[0]['message']}

  Memory entries: {memory.count()}
""")

    # Commit frequency
    commits = get_git_log(100)
    dates = {}
    for c in commits:
        d = c["date"][:10]
        dates[d] = dates.get(d, 0) + 1
    avg = sum(dates.values()) / max(len(dates), 1)
    print(f"  Avg commits/day (last 100): {avg:.1f}")


def cmd_add_context(args, memory: Memory):
    """Add a note to git memory."""
    memory.add(
        args.text,
        metadata={
            "source": "git-context",
            "category": args.category or "general",
            "git_hash": run("git rev-parse HEAD")[:12],
        }
    )
    print(f"✅ Added to memory: {args.text[:60]}")


def cmd_diff(args, memory: Memory):
    """Show diff for a commit."""
    if args.commit:
        out = run(f"git show {args.commit}")
        print(out)
    else:
        out = run("git diff HEAD~1")
        print(out or "[no changes]")


def main():
    parser = argparse.ArgumentParser(
        description="git-memory: Ask questions about your git history"
    )
    # Memory args — before subparsers
    parser.add_argument("--storage", default="json")
    parser.add_argument("--path", default="./git_memory.json")

    sub = parser.add_subparsers(dest="cmd")

    ask = sub.add_parser("ask", help="Ask a question about git history")
    ask.add_argument("question", nargs="+", help="Question to answer")

    log = sub.add_parser("log", help="Show recent commits")
    log.add_argument("--limit", "-n", type=int, default=10)

    stats = sub.add_parser("stats", help="Show git statistics")

    ctx = sub.add_parser("add-context", help="Add context to memory")
    ctx.add_argument("text", help="Context text to remember")
    ctx.add_argument("--category", "-c", help="Category tag")

    diff = sub.add_parser("diff", help="Show diff")
    diff.add_argument("--commit", "-c", help="Commit hash")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return

    memory = Memory(storage=args.storage, path=args.path)

    if args.cmd == "ask":
        q = " ".join(args.question)
        cmd_ask(memory, q)
    elif args.cmd == "log":
        cmd_log(args, memory)
    elif args.cmd == "stats":
        cmd_stats(args, memory)
    elif args.cmd == "add-context":
        cmd_add_context(args, memory)
    elif args.cmd == "diff":
        cmd_diff(args, memory)


if __name__ == "__main__":
    main()
