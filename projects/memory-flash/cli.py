#!/usr/bin/env python3
"""
Memory Flash — Quick memory flash between sessions
A CLI to quickly add/view memories without full setup.
"""

import argparse
import json
import os
import sys
from datetime import datetime

DEFAULT_PATH = os.path.expanduser("~/.agent-memory-flash.json")

def add_memory(text, path=None):
    """Add a quick memory."""
    path = path or DEFAULT_PATH
    
    memories = []
    if os.path.exists(path):
        with open(path, "r") as f:
            memories = json.load(f)
    
    memory = {
        "id": len(memories) + 1,
        "text": text,
        "created_at": datetime.now().isoformat(),
        "tags": []
    }
    
    # Auto-tag based on keywords
    text_lower = text.lower()
    if "bug" in text_lower or "error" in text_lower or "fix" in text_lower:
        memory["tags"].append("bug")
    if "idea" in text_lower or "thought" in text_lower:
        memory["tags"].append("idea")
    if "todo" in text_lower or "will" in text_lower:
        memory["tags"].append("todo")
    
    memories.append(memory)
    
    with open(path, "w") as f:
        json.dump(memories, f, indent=2)
    
    print(f"✅ Added memory #{memory['id']}: {text[:50]}...")
    return memory

def list_memories(path=None, tag=None):
    """List all memories."""
    path = path or DEFAULT_PATH
    
    if not os.path.exists(path):
        print("No memories yet. Use 'add' to create one.")
        return
    
    with open(path, "r") as f:
        memories = json.load(f)
    
    if tag:
        memories = [m for m in memories if tag in m.get("tags", [])]
    
    if not memories:
        print("No memories found.")
        return
    
    print(f"📝 {len(memories)} memories:\n")
    for m in memories:
        tags = f" [{', '.join(m.get('tags', []))}]" if m.get("tags") else ""
        created = m.get("created_at", "")[:10]
        print(f"  #{m['id']} [{created}]{tags}")
        print(f"     {m['text'][:70]}...")
        print()

def search_memories(query, path=None):
    """Search memories."""
    path = path or DEFAULT_PATH
    
    if not os.path.exists(path):
        print("No memories yet.")
        return
    
    with open(path, "r") as f:
        memories = json.load(f)
    
    results = [m for m in memories if query.lower() in m["text"].lower()]
    
    if not results:
        print(f"No memories found matching '{query}'.")
        return
    
    print(f"🔍 Found {len(results)} results:\n")
    for m in results:
        print(f"  #{m['id']} {m['text'][:70]}...")

def clear_memories(path=None):
    """Clear all memories."""
    path = path or DEFAULT_PATH
    
    if not os.path.exists(path):
        print("No memories to clear.")
        return
    
    confirm = input(f"Delete {path}? (y/N): ")
    if confirm.lower() == "y":
        os.remove(path)
        print("✅ Cleared all memories.")

def main():
    parser = argparse.ArgumentParser(
        description="Memory Flash — Quick memory CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # add
    add_parser = subparsers.add_parser("add", help="Add a memory")
    add_parser.add_argument("text", help="Memory text")
    add_parser.add_argument("-p", "--path", help="Custom memory file path")
    
    # list
    list_parser = subparsers.add_parser("list", help="List memories")
    list_parser.add_argument("-p", "--path", help="Custom memory file path")
    list_parser.add_argument("-t", "--tag", help="Filter by tag")
    
    # search
    search_parser = subparsers.add_parser("search", help="Search memories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("-p", "--path", help="Custom memory file path")
    
    # clear
    clear_parser = subparsers.add_parser("clear", help="Clear all memories")
    clear_parser.add_argument("-p", "--path", help="Custom memory file path")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_memory(args.text, args.path)
    elif args.command == "list":
        list_memories(args.path, args.tag)
    elif args.command == "search":
        search_memories(args.query, args.path)
    elif args.command == "clear":
        clear_memories(args.path)

if __name__ == "__main__":
    main()
