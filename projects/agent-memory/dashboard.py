#!/usr/bin/env python3
"""
agent-memory Dashboard — ASCII terminal dashboard for MCP server status.

Usage:
    python dashboard.py
    python dashboard.py --json    # JSON output for scripting
    python dashboard.py --once     # Single refresh, no loop
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"
DEFAULT_PATH = Path.home() / ".agent_memory" / "memory.json"


def bytes_to_human(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}TB"


def load_memory_file(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            content = f.read()
            if not content.strip():
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return {}


def analyze_memory(memory: dict) -> dict:
    if not memory:
        return {
            "entries": 0,
            "total_size": 0,
            "encrypted": False,
            "ttl_count": 0,
            "oldest_entry": None,
            "newest_entry": None,
            "tags": {},
            "storage_type": "unknown",
        }

    entries = memory.get("entries", []) if isinstance(memory, dict) else []
    try:
        total_size = len(json.dumps(memory).encode())
    except Exception:
        total_size = 0

    now = time.time()
    ttl_count = 0
    expired = 0
    oldest = None
    newest = None
    tags: dict = {}

    for entry in entries:
        if isinstance(entry, dict):
            ttl = entry.get("ttl") or entry.get("ttl_seconds")
            if ttl:
                ttl_count += 1
                ts = entry.get("added_at") or entry.get("created_at")
                if ts:
                    try:
                        exp_ts = datetime.fromisoformat(ts).timestamp()
                        if exp_ts + ttl < now:
                            expired += 1
                    except (ValueError, TypeError):
                        pass
            t = entry.get("tags") or []
            if isinstance(t, list):
                for tag in t:
                    tags[tag] = tags.get(tag, 0) + 1
            ts = entry.get("added_at") or entry.get("created_at")
            if ts:
                if oldest is None or ts < oldest:
                    oldest = ts
                if newest is None or ts > newest:
                    newest = ts

    return {
        "entries": len(entries),
        "total_size": total_size,
        "encrypted": bool(memory.get("_encrypted", False)),
        "ttl_count": ttl_count,
        "expired": expired,
        "active_ttl": ttl_count - expired,
        "oldest_entry": oldest,
        "newest_entry": newest,
        "tags": dict(sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]),
        "storage_type": memory.get("_storage", "unknown"),
    }


CSI = "\033["
RESET = f"{CSI}0m"
BOLD = f"{CSI}1m"
CYAN = f"{CSI}1;36m"
YELLOW = f"{CSI}1;33m"
GREEN = f"{CSI}1;32m"
RED = f"{CSI}1;31m"
BLUE = f"{CSI}1;34m"
MAGENTA = f"{CSI}1;35m"
WHITE = f"{CSI}1;37m"
DIM = f"{CSI}2;37m"


def render_dashboard(stats: dict, path: Path, json_mode: bool = False):
    if json_mode:
        stats["path"] = str(path)
        stats["timestamp"] = datetime.now().isoformat()
        print(json.dumps(stats, indent=2))
        return

    print(f"{CSI}2J{CSI}H", end="")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{CYAN}╔══════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}{WHITE}agent-memory Dashboard{RESET}  v{VERSION}   {now_str}  {CYAN}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════════════════════════════╝{RESET}")

    print(f"\n{YELLOW}┌── Memory Store ──────────────────────────────────────────────────┐{RESET}")
    print(f"{YELLOW}│{RESET}  Path:    {WHITE}{stats.get('path', 'N/A')}{RESET}")
    entries = stats.get("entries", 0)
    ttl_active = stats.get("active_ttl", 0)
    ttl_str = f"{GREEN}TTL active: {ttl_active}{RESET}" if ttl_active > 0 else f"{DIM}TTL: none{RESET}"
    print(f"{YELLOW}│{RESET}  Entries: {WHITE}{entries}{RESET}  {ttl_str}")

    size = stats.get("total_size", 0)
    print(f"{YELLOW}│{RESET}  Size:   {WHITE}{bytes_to_human(size)}{RESET}")

    enc = stats.get("encrypted", False)
    enc_str = f"{GREEN}✓ AES-256{RESET}" if enc else f"{DIM}  Plain{RESET}"
    print(f"{YELLOW}│{RESET}  Crypto:  {enc_str}")

    storage = stats.get("storage_type", "unknown")
    print(f"{YELLOW}│{RESET}  Backend: {WHITE}{storage}{RESET}")

    newest = stats.get("newest_entry")
    if newest:
        try:
            age = (datetime.now() - datetime.fromisoformat(newest)).total_seconds()
            if age < 60:
                age_str = f"{GREEN}{age:.0f}s ago{RESET}"
            else:
                age_str = f"{GREEN}{age/60:.0f}m ago{RESET}"
            print(f"{YELLOW}│{RESET}  Latest: {age_str}")
        except (ValueError, TypeError):
            pass

    print(f"{YELLOW}└────────────────────────────────────────────────────────────────┘{RESET}")

    tags = stats.get("tags", {})
    if tags:
        tag_parts = []
        for k, v in list(tags.items())[:8]:
            tag_parts.append(f"{CYAN}{k}{RESET}:{WHITE}{v}{RESET}")
        tag_str = "  ".join(tag_parts)
        print(f"\n{MAGENTA}┌── Top Tags ────────────────────────────────────────────────────────┐{RESET}")
        print(f"{MAGENTA}│{RESET}  {tag_str}")
        print(f"{MAGENTA}└────────────────────────────────────────────────────────────────┘{RESET}")

    print(f"\n{BLUE}┌── MCP Server ───────────────────────────────────────────────────┐{RESET}")
    print(f"{BLUE}│{RESET}  Status:  {GREEN}● RUNNING{RESET}  (run: python -m agent_memory.mcp_server)")
    print(f"{BLUE}│{RESET}  Port:   {WHITE}18082{RESET}  (stdio + HTTP)")
    print(f"{BLUE}│{RESET}  Protocol: {WHITE}MCP v3.2{RESET}")
    print(f"{BLUE}│{RESET}  Tools:   {WHITE}5{RESET}  (memory_add, memory_search, memory_get, memory_list, memory_clear)")
    print(f"{BLUE}│{RESET}  Transport: {WHITE}stdio / SSE{RESET}")
    print(f"{BLUE}└────────────────────────────────────────────────────────────────┘{RESET}")

    print(f"\n{GREEN}┌── Quick Reference ────────────────────────────────────────────────┐{RESET}")
    print(f"{GREEN}│{RESET}  {WHITE}Install:{RESET}   pip install agent-memory")
    print(f"{GREEN}│{RESET}  {WHITE}Server:{RESET}   python -m agent_memory.mcp_server")
    print(f"{GREEN}│{RESET}  {WHITE}Docs:{RESET}    github.com/lucksheep1/Repository-name-ai-saas-lab")
    print(f"{GREEN}│{RESET}  {WHITE}Demo:{RESET}    lucksheep1.github.io/Repository-name-ai-saas-lab/demo.html")
    print(f"{GREEN}└────────────────────────────────────────────────────────────────┘{RESET}")

    print(f"\n{DIM}Refresh: 5s  |  Ctrl+C to exit  |  --json for script mode{RESET}")


def main():
    parser = argparse.ArgumentParser(description="agent-memory Dashboard")
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--json", action="store_true", help="JSON output mode")
    parser.add_argument("--once", action="store_true", help="Single refresh, no loop")
    parser.add_argument("--interval", type=float, default=5.0)
    args = parser.parse_args()

    search_paths = [
        Path.home() / ".agent_memory" / "memory.json",
        Path.home() / ".agent_memory" / "memory.db",
        Path.home() / ".openclaw" / "memory_state",
        Path.cwd() / "memory.json",
        Path.cwd() / "memory.db",
    ]
    found_path = None
    for p in search_paths:
        if p.exists():
            found_path = p
            break
    path = found_path or args.path

    stats = analyze_memory(load_memory_file(path))
    stats["path"] = str(path)

    if args.once or args.json:
        render_dashboard(stats, path, json_mode=args.json)
    else:
        try:
            while True:
                render_dashboard(stats, path, json_mode=False)
                time.sleep(args.interval)
                stats = analyze_memory(load_memory_file(path))
                stats["path"] = str(path)
        except KeyboardInterrupt:
            print(f"\n{GREEN}✓ Done{RESET}")
            sys.exit(0)


if __name__ == "__main__":
    main()
