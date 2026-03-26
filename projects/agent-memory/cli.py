#!/usr/bin/env python3
"""
Agent Memory CLI - Command-line interface for agent-memory.

Usage:
    agent-memory init                    Initialize a memory store
    agent-memory add "text"            Add a memory
    agent-memory search "query"         Search memories
    agent-memory list                  List all memories
    agent-memory delete <id>          Delete a memory
    agent-memory clear                 Clear all memories
    agent-memory stats                 Show memory statistics

Environment:
    AGENT_MEMORY_PATH    Path to memory file (default: ./memory.json)
    AGENT_MEMORY_TTL     Default TTL for memories (e.g., "7d")
    AGENT_MEMORY_KEY      Encryption key
"""
import sys
import argparse
import os


def get_memory():
    from agent_memory import Memory
    path = os.environ.get("AGENT_MEMORY_PATH", "./memory.json")
    ttl = os.environ.get("AGENT_MEMORY_TTL")
    key = os.environ.get("AGENT_MEMORY_KEY")
    storage = "json"
    if path.endswith(".db"):
        storage = "sqlite"
    kwargs = {"storage": storage, "path": path}
    if ttl:
        kwargs["ttl"] = ttl
    if key:
        kwargs["encryption_key"] = key
    return Memory(**kwargs)


def cmd_init(args):
    path = os.environ.get("AGENT_MEMORY_PATH", "./memory.json")
    m = get_memory()
    m.add("initialized", metadata={"system": "init"})
    print(f"Initialized: {path}")
    return 0


def cmd_add(args):
    m = get_memory()
    kwargs = {}
    if args.ttl:
        kwargs["ttl"] = args.ttl
    if args.encrypt:
        kwargs["encrypt"] = True
    mid = m.add(args.text, metadata=kwargs)
    print(f"Added: {mid}")
    return 0


def cmd_search(args):
    m = get_memory()
    results = m.search(args.query, top_k=args.top_k)
    if not results:
        print("No results found.")
        return 0
    for r in results:
        sim = r.get("similarity", 0)
        tags = r.get("tags", [])
        expires = r.get("expires_at", "never")
        print(f"  [{r['id']}] (sim={sim:.2f}) {r['text'][:80]}")
        if tags:
            print(f"       tags: {tags}")
        if expires != "never":
            print(f"       expires: {expires}")
    return 0


def cmd_list(args):
    m = get_memory()
    memories = m.memories
    if not memories:
        print("No memories stored.")
        return 0
    print(f"Total: {len(memories)} memories")
    for r in memories:
        tags = r.get("tags", [])
        expires = r.get("expires_at", "never")
        print(f"  [{r['id']}] {r['text'][:60]}")
        if tags:
            print(f"       tags: {tags}")
        if expires != "never":
            print(f"       expires: {expires}")
    return 0


def cmd_delete(args):
    m = get_memory()
    if m.delete(args.memory_id):
        print(f"Deleted: {args.memory_id}")
        return 0
    else:
        print(f"Not found: {args.memory_id}")
        return 1


def cmd_clear(args):
    m = get_memory()
    count = len(m.memories)
    m.clear()
    print(f"Cleared {count} memories.")
    return 0


def cmd_stats(args):
    m = get_memory()
    total = len(m.memories)
    encrypted = sum(1 for x in m.memories if x.get("metadata", {}).get("encrypted"))
    with_expiry = sum(1 for x in m.memories if x.get("expires_at"))
    print(f"Total memories: {total}")
    print(f"Encrypted: {encrypted}")
    print(f"With expiry: {with_expiry}")
    print(f"Storage: {m.storage}")
    return 0


def cmd_context(args):
    m = get_memory()
    ctx = m.get_context(max_tokens=args.max_tokens, max_memories=args.max_memories)
    print(ctx)
    return 0


def cmd_export(args):
    m = get_memory()
    m.export(args.output)
    print(f"✅ Exported {m.count()} memories to {args.output}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="agent-memory",
        description="Agent Memory CLI - Lightweight memory for AI agents"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="Initialize memory store")
    
    add_parser = sub.add_parser("add", help="Add a memory")
    add_parser.add_argument("text", help="Memory text")
    add_parser.add_argument("--ttl", help="TTL e.g. '7d', '1h', '30m'")
    add_parser.add_argument("--encrypt", action="store_true", help="Encrypt this memory")

    search_parser = sub.add_parser("search", help="Search memories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--top-k", type=int, default=5, help="Number of results")

    sub.add_parser("list", help="List all memories")
    
    del_parser = sub.add_parser("delete", help="Delete a memory")
    del_parser.add_argument("memory_id", help="Memory ID to delete")

    sub.add_parser("clear", help="Clear all memories")

    sub.add_parser("stats", help="Show statistics")

    ctx_parser = sub.add_parser("context", help="Get conversation context for LLM")
    ctx_parser.add_argument("--max-tokens", type=int, default=2000, dest="max_tokens")
    ctx_parser.add_argument("--max-memories", type=int, default=10, dest="max_memories")

    exp_parser = sub.add_parser("export", help="Export memories to file")
    exp_parser.add_argument("output", help="Output file path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "search": cmd_search,
        "list": cmd_list,
        "delete": cmd_delete,
        "clear": cmd_clear,
        "stats": cmd_stats,
        "context": cmd_context,
        "export": cmd_export,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
