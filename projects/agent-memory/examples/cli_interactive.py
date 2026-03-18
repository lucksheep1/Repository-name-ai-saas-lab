#!/usr/bin/env python3
"""
Agent Memory - CLI with Interactive Mode
========================================
Interactive CLI for memory management.

Usage:
    python cli_interactive.py
    
    Commands:
      add <text>          - Add memory
      search <query>      - Search memories
      recent              - Show recent memories
      context             - Get context
      tags                - List all tags
      stats               - Show statistics
      help                - Show help
      quit                - Exit
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import shlex
from agent_memory import Memory


def print_header():
    """Print header."""
    print("=" * 50)
    print("🤖 Agent Memory - Interactive CLI")
    print("=" * 50)
    print()


def print_help():
    """Print help."""
    print("""
Commands:
  add <text>          - Add memory
  addt <text> <tag1> <tag2>... - Add with tags
  search <query>      - Search memories
  recent [limit]      - Show recent memories (default: 10)
  context [tokens]    - Get context (default: 2000)
  tags                - List all tags
  by-tag <tag>        - Get memories by tag
  stats               - Show statistics
  clear               - Clear all memories
  help                - Show this help
  quit                - Exit
""")


def main():
    """Run interactive CLI."""
    memory = Memory(storage="json", path="./memory.json")
    
    print_header()
    print_help()
    
    while True:
        try:
            cmd = input("\n> ").strip()
            
            if not cmd:
                continue
            
            # Parse command
            parts = shlex.split(cmd)
            command = parts[0].lower()
            args = parts[1:]
            
            if command in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            
            elif command == "help":
                print_help()
            
            elif command == "add":
                if not args:
                    print("Usage: add <text>")
                    continue
                text = " ".join(args)
                memory_id = memory.add(text)
                print(f"✓ Added: {memory_id}")
            
            elif command == "addt":
                if len(args) < 2:
                    print("Usage: addt <text> <tag1> <tag2> ...")
                    continue
                text = args[0]
                tags = args[1:]
                memory_id = memory.add_with_tags(text, tags=tags)
                print(f"✓ Added with tags {tags}: {memory_id}")
            
            elif command == "search":
                if not args:
                    print("Usage: search <query>")
                    continue
                query = " ".join(args)
                results = memory.search(query)
                print(f"Found {len(results)} results:")
                for r in results:
                    print(f"  - {r['text'][:60]}")
            
            elif command == "recent":
                limit = int(args[0]) if args else 10
                recent = memory.get_recent(limit=limit)
                print(f"Recent {len(recent)} memories:")
                for r in recent:
                    tags = r.get("tags", [])
                    tag_str = f" [{', '.join(tags)}]" if tags else ""
                    print(f"  - {r['text'][:60]}{tag_str}")
            
            elif command == "context":
                max_tokens = int(args[0]) if args else 2000
                context = memory.get_context(max_tokens=max_tokens)
                print(context)
            
            elif command == "tags":
                recent = memory.get_recent(limit=memory.count())
                all_tags = set()
                for r in recent:
                    all_tags.update(r.get("tags", []))
                print(f"Tags ({len(all_tags)}): {', '.join(sorted(all_tags))}")
            
            elif command == "by-tag":
                if not args:
                    print("Usage: by-tag <tag>")
                    continue
                tag = args[0]
                results = memory.get_by_tag(tag)
                print(f"Found {len(results)} memories with tag '{tag}':")
                for r in results:
                    print(f"  - {r['text'][:60]}")
            
            elif command == "stats":
                print(f"Total memories: {memory.count()}")
            
            elif command == "clear":
                confirm = input("Clear all memories? (y/n) ")
                if confirm.lower() == "y":
                    memory.clear()
                    print("✓ Cleared all memories")
            
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
