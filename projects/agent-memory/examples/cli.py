#!/usr/bin/env python3
"""
Agent Memory - CLI
==================
Command-line interface for agent-memory.

Usage:
    python cli.py add "Remember this"
    python cli.py search "remember"
    python cli.py context
    python cli.py recent
    python cli.py stats
"""

import sys
import os
import argparse
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory


def main():
    parser = argparse.ArgumentParser(description="Agent Memory CLI")
    parser.add_argument("command", choices=["add", "search", "context", "recent", "stats", "timeline", "by-tag", "by-priority", "clear", "export", "import"])
    parser.add_argument("--text", help="Text for add/search")
    parser.add_argument("--query", help="Query for search")
    parser.add_argument("--tag", help="Tag for by-tag")
    parser.add_argument("--priority", type=int, help="Priority threshold for by-priority")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--limit", type=int, default=10, help="Limit results")
    parser.add_argument("--max-tokens", type=int, default=2000, help="Max tokens for context")
    parser.add_argument("--file", help="File for export/import")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Export format")
    parser.add_argument("--storage", default="json", help="Storage backend")
    parser.add_argument("--path", default="./memory.json", help="Memory file path")
    
    args = parser.parse_args()
    
    # Initialize memory
    memory = Memory(storage=args.storage, path=args.path)
    
    if args.command == "add":
        if not args.text:
            print("Error: --text required for add")
            sys.exit(1)
        memory_id = memory.add(args.text)
        print(f"Added: {memory_id}")
    
    elif args.command == "search":
        query = args.text or args.query
        if not query:
            print("Error: --text or --query required for search")
            sys.exit(1)
        results = memory.search(query, top_k=args.top_k)
        print(json.dumps(results, indent=2, default=str))
    
    elif args.command == "context":
        context = memory.get_context(max_tokens=args.max_tokens)
        print(context)
    
    elif args.command == "recent":
        recent = memory.get_recent(limit=args.limit)
        print(json.dumps(recent, indent=2, default=str))
    
    elif args.command == "stats":
        stats = {
            "count": memory.count(),
            "storage": args.storage,
            "path": args.path
        }
        print(json.dumps(stats, indent=2))
    
    elif args.command == "timeline":
        timeline = memory.get_timeline(limit=args.limit)
        print(json.dumps(timeline, indent=2, default=str))
    
    elif args.command == "by-tag":
        if not args.tag:
            print("Error: --tag required for by-tag")
            sys.exit(1)
        results = memory.get_by_tag(args.tag)
        print(json.dumps(results, indent=2, default=str))
    
    elif args.command == "by-priority":
        if args.priority is None:
            print("Error: --priority required for by-priority")
            sys.exit(1)
        results = memory.get_by_priority(args.priority)
        print(json.dumps(results, indent=2, default=str))
    
    elif args.command == "clear":
        memory.clear()
        print("Memory cleared")
    
    elif args.command == "export":
        if not args.file:
            print("Error: --file required for export")
            sys.exit(1)
        if args.format == "markdown":
            memory.export_markdown(args.file)
            print(f"Exported to Markdown: {args.file}")
        else:
            memory.export(args.file)
            print(f"Exported to JSON: {args.file}")
    
    elif args.command == "import":
        if not args.file:
            print("Error: --file required for import")
            sys.exit(1)
        memory.import_(args.file)
        print(f"Imported from: {args.file}")


if __name__ == "__main__":
    main()
