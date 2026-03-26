#!/usr/bin/env python3
"""
skill-builder: Generate OpenClaw SKILL.md files from templates.

Creates properly formatted SKILL.md for the OpenClaw skill ecosystem,
following the format established by linux-server-skill.

Usage:
    python skill_builder.py list
    python skill_builder.py new <skill-name> --template <template>
    python skill_builder.py generate <skill-name> --desc "<description>" --triggers "<triggers>"
"""

import argparse
import os
import sys
from pathlib import Path

SKILL_TEMPLATES = {
    "memory": {
        "name": "agent-memory-ops",
        "description": "Manage persistent memory for AI agents. Store, search, and recall information across sessions. Supports TTL expiration, encryption, tagging, and multiple storage backends (JSON/SQLite/Redis). Use when: the user wants to remember something across conversations, search past information, set time-based memory expiration, encrypt sensitive data, or manage knowledge bases.",
        "triggers": ["remember", "recall", "forget", "search memory", "what do you know", "memory", "persist"],
        "sections": [
            ("SENSITIVE DATA", "No sensitive data stored by default. User memory is stored locally. Encryption available via --encryption-key flag."),
            ("Session Start", "Check workspace for existing memory store (memory.json, memory.db). Report memory count on startup."),
            ("Commands", "- `add <text>` — store a memory with optional TTL (e.g. '1h', '7d')\n- `search <query>` — find relevant memories\n- `list` — show recent memories\n- `clear [--all]` — clear memories"),
        ],
    },
    "git": {
        "name": "git-history-ops",
        "description": "Query and analyze git repository history. Answer questions about commits, contributors, file changes, and patterns. Use natural language to ask about: 'what changed last week', 'who made the most commits', 'show me all bug fixes', 'what files are most frequently changed', 'commits on a specific date'.",
        "triggers": ["git history", "commit", "what changed", "who committed", "git log", "git blame", "diff", "branch"],
        "sections": [
            ("SENSITIVE DATA", "Git history is typically public. Never expose: private file paths on local machine, SSH keys in commit metadata, secrets accidentally committed."),
            ("Session Start", "Run `git log --oneline -20` to show recent activity. Identify main branch and any active feature branches."),
            ("Commands", "- `ask '<question>'` — natural language git queries\n- `log [--limit N]` — show recent commits\n- `stats` — commit frequency, contributor stats\n- `add-context <note>` — store important git context in agent-memory"),
        ],
    },
    "search": {
        "name": "web-search-ops",
        "description": "Search the web for real-time information. Use Brave Search API for AI-optimized results. Use when: the user asks about current events, needs factual verification, wants to find documentation, or research a topic.",
        "triggers": ["search", "find on web", "look up", "what is", "who is", "current news", "latest", "google"],
        "sections": [
            ("SENSITIVE DATA", "Search queries are sent to Brave Search API. No authentication credentials stored. User IP visible to Brave."),
            ("Session Start", "Confirm Brave Search API key is configured in environment (BRAVE_SEARCH_KEY). If missing, inform user."),
            ("Commands", "- `search <query>` — web search with Brave API\n- `fetch <url>` — extract readable content from URL\n- `summarize <url>` — summarize URL content"),
        ],
    },
    "server": {
        "name": "linux-server-ops",
        "description": "Manage Linux servers via SSH. Deploy websites, configure databases, set up SSL certificates, manage Docker containers, monitor resources, and configure Nginx. Use when: the user wants to deploy a service, check server status, restart a service, configure SSL, or manage Docker.",
        "triggers": ["deploy", "server", "ssh", "linux", "ssl", "nginx", "docker", "database", "restart service", "monitor"],
        "sections": [
            ("SENSITIVE DATA", "CRITICAL: Never display server IPs, SSH keys, or passwords. Always use server ID (e.g., 'prod-web') instead of IP. Mask all secrets in output."),
            ("Session Start", "Check for .server/servers.json and .server/snapshots/. Load existing server context before making changes."),
            ("Commands", "- `status <server-id>` — check server resources\n- `deploy <server-id> <service>` — deploy service\n- `ssl <domain>` — provision SSL certificate\n- `docker ps <server-id>` — list containers\n- `restart <service>` — restart a service"),
        ],
    },
    "monitor": {
        "name": "system-monitor",
        "description": "Monitor system resources and receive alerts. Track CPU, memory, disk, network, and running processes. Set up threshold-based alerts. Use when: the user wants to check system health, set up monitoring, investigate high resource usage, or review process lists.",
        "triggers": ["monitor", "cpu", "memory", "disk", "process", "alert", "resource", "usage", "system health"],
        "sections": [
            ("SENSITIVE DATA", "System monitoring shows resource usage. Process lists may reveal software installed. No personal user data exposed."),
            ("Session Start", "Run `top -bn1 | head -20` for quick process overview. Run `df -h` for disk, `free -m` for memory."),
            ("Commands", "- `status` — CPU, memory, disk overview\n- `processes [--top N]` — top N processes by CPU/memory\n- `disk` — disk usage for all mounts\n- `network` — active network connections\n- `alert <metric> <threshold>` — set up alert"),
        ],
    },
    "scrape": {
        "name": "web-scraper",
        "description": "Extract structured data from websites. Fetch and parse HTML into readable text, extract specific elements, take screenshots. Use when: the user wants to extract data from a webpage, monitor a page for changes, or capture content from a URL.",
        "triggers": ["scrape", "extract", "fetch content", "parse html", "web page", "screenshot", "crawl"],
        "sections": [
            ("SENSITIVE DATA", "Web scraping may be subject to robots.txt and Terms of Service. Always check before scraping. No credentials needed for public pages."),
            ("Session Start", "Use web_fetch for simple content extraction. Use browser tool for JavaScript-rendered pages or interactive content."),
            ("Commands", "- `fetch <url>` — extract readable text from URL\n- `screenshot <url>` — capture page screenshot\n- `extract <url> --selector <css>` — extract specific DOM elements"),
        ],
    },
}


def generate_skill_md(name: str, description: str, triggers: list, extra_sections: list = None) -> str:
    """Generate a SKILL.md file content."""
    triggers_str = ", ".join(triggers) if triggers else ""

    sections_md = ""
    if extra_sections:
        for title, content in extra_sections:
            sections_md += f"\n## {title}\n\n{content}\n"

    return f"""---
name: {name}
description: {description}
---

# {name.replace('-', ' ').title()}

## When to Use

Use this skill when the user mentions: {triggers_str}.

{sections_md}
## Quality Standards

- Always verify destructive operations before executing
- Report progress clearly during long-running tasks
- Mask all sensitive data in output
- Maintain context between commands in a session
"""


def cmd_list():
    """List available templates."""
    print("\n📦 Available skill templates:\n")
    for key, tpl in SKILL_TEMPLATES.items():
        print(f"  {key:12} — {tpl['description'][:60]}...")
    print()


def cmd_new(args):
    """Generate a new skill from template."""
    skill_key = args.template or args.name

    if skill_key in SKILL_TEMPLATES:
        tpl = SKILL_TEMPLATES[skill_key]
        desc = args.desc or tpl["description"]
        triggers = args.triggers.split(",") if args.triggers else tpl["triggers"]
        sections = tpl.get("sections", [])
        name = args.name if args.name != skill_key else tpl["name"]
    else:
        # Custom skill
        name = args.name or "custom-skill"
        desc = args.desc or "Custom skill for OpenClaw"
        triggers = [t.strip() for t in (args.triggers or "").split(",") if t.strip()]
        sections = []

    output_dir = Path(args.output) if args.output else Path(f"skills/{name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "SKILL.md"

    md = generate_skill_md(name, desc, triggers, sections)

    with open(output_path, "w") as f:
        f.write(md)

    print(f"✅ Skill generated: {output_path}")
    print(f"   Name: {name}")
    print(f"   Triggers: {', '.join(triggers[:5])}")
    print(f"\nTo install: move {output_path} to your OpenClaw skills directory")


def cmd_generate(args):
    """Generate a skill with full customization."""
    name = args.name.lower().replace(" ", "-")
    desc = args.desc
    triggers = [t.strip() for t in (args.triggers or "").split(",") if t.strip()]

    output_path = Path(args.output or f"skills/{name}/SKILL.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    md = generate_skill_md(name, desc, triggers)
    with open(output_path, "w") as f:
        f.write(md)

    print(f"✅ Generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="skill-builder: Generate OpenClaw SKILL.md files")
    sub = parser.add_subparsers(dest="cmd")

    # list command
    sub.add_parser("list", help="List available skill templates")

    # new command
    new_parser = sub.add_parser("new", help="Generate a new skill from template")
    new_parser.add_argument("name", help="Skill name or template key")
    new_parser.add_argument("--template", "-t", help="Template to use (overrides name)")
    new_parser.add_argument("--desc", "-d", help="Skill description")
    new_parser.add_argument("--triggers", help="Comma-separated trigger phrases")
    new_parser.add_argument("--output", "-o", help="Output directory or file path")

    # generate command
    gen_parser = sub.add_parser("generate", help="Generate a fully custom skill")
    gen_parser.add_argument("name", help="Skill name (kebab-case)")
    gen_parser.add_argument("--desc", "-d", required=True, help="Skill description")
    gen_parser.add_argument("--triggers", help="Comma-separated trigger phrases")
    gen_parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        print("\n📦 Available templates:")
        cmd_list()
        return

    if args.cmd == "list":
        cmd_list()
    elif args.cmd == "new":
        cmd_new(args)
    elif args.cmd == "generate":
        cmd_generate(args)


if __name__ == "__main__":
    main()
