#!/usr/bin/env python3
"""
agent-memory backup/restore CLI

Usage:
    # Backup all memories to a file
    python memory_backup.py backup --storage json --path ./memory.json --output backup.json

    # Restore from backup
    python memory_backup.py restore --storage json --path ./memory.json --input backup.json

    # Stats (no modification)
    python memory_backup.py stats --storage json --path ./memory.json
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from agent_memory import Memory, _UNSET


def backup(storage: str, path: str, output: str, ttl: str = None, encryption_key: str = None):
    """Export all memories to a JSON backup file."""
    m = Memory(storage=storage, path=path, ttl=ttl, encryption_key=encryption_key)
    
    all_memories = m.memories
    metadata = {
        "version": "1.0",
        "storage": storage,
        "path": path,
        "count": len(all_memories),
    }
    
    backup_data = {
        "metadata": metadata,
        "memories": all_memories,
    }
    
    with open(output, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Backed up {len(all_memories)} memories to {output}")
    return 0


def restore(storage: str, path: str, input: str, ttl: str = None, encryption_key: str = None):
    """Restore memories from a JSON backup file."""
    m = Memory(storage=storage, path=path, ttl=ttl, encryption_key=encryption_key)
    
    with open(input, encoding="utf-8") as f:
        backup_data = json.load(f)
    
    memories = backup_data.get("memories", [])
    metadata = backup_data.get("metadata", {})
    
    restored = 0
    from datetime import datetime
    for mem in memories:
        text = mem.get("text", "")
        metadata_mem = mem.get("metadata", {})
        is_encrypted = metadata_mem.get("encrypted", False)
        
        # TTL: convert expires_at back to TTL string
        ttl_mem = _UNSET
        if mem.get("expires_at"):
            exp = datetime.fromisoformat(mem["expires_at"])
            remaining = (exp - datetime.now()).total_seconds()
            if remaining > 0:
                ttl_mem = f"{int(remaining // 60)}m"
        
        if text:
            m.add(text=text, metadata=metadata_mem, ttl=ttl_mem, encrypt=is_encrypted)
            restored += 1
    
    print(f"✅ Restored {restored} memories from {input}")
    return 0


def stats(storage: str, path: str, ttl: str = None, encryption_key: str = None):
    """Show memory statistics without modifying anything."""
    m = Memory(storage=storage, path=path, ttl=ttl, encryption_key=encryption_key)
    
    all_memories = m.memories
    count = len(all_memories)
    
    # Count encrypted
    encrypted = sum(1 for mem in all_memories if mem.get("metadata", {}).get("encrypted"))
    
    # Count with TTL
    with_ttl = sum(1 for mem in all_memories if mem.get("expires_at"))
    
    # Storage type
    storage_labels = {"json": "JSON file", "sqlite": "SQLite", "redis": "Redis"}
    storage_label = storage_labels.get(storage, storage)
    
    print(f"📊 Memory Statistics")
    print(f"   Storage: {storage_label} ({path})")
    print(f"   Total memories: {count}")
    print(f"   Encrypted: {encrypted}")
    print(f"   With TTL: {with_ttl}")
    print(f"   Plain text: {count - encrypted}")
    
    return 0


def main():
    parser = argparse.ArgumentParser(description="agent-memory backup/restore/Stats")
    sub = parser.add_subparsers(dest="command", required=True)
    
    for cmd, fn in [("backup", backup), ("restore", restore), ("stats", stats)]:
        p = sub.add_parser(cmd)
        p.add_argument("--storage", default="json", choices=["json", "sqlite", "redis"])
        p.add_argument("--path", default="./memory.json")
        p.add_argument("--ttl", default=None)
        p.add_argument("--encryption-key", default=None, dest="encryption_key")
        
        if cmd == "backup":
            p.add_argument("--output", required=True)
        elif cmd == "restore":
            p.add_argument("--input", required=True)
    
    args = parser.parse_args()
    
    fn = {"backup": backup, "restore": restore, "stats": stats}[args.command]
    if args.command == "backup":
        return fn(args.storage, args.path, args.output, args.ttl, args.encryption_key)
    elif args.command == "restore":
        return fn(args.storage, args.path, args.input, args.ttl, args.encryption_key)
    else:
        return fn(args.storage, args.path, args.ttl, args.encryption_key)


if __name__ == "__main__":
    sys.exit(main())
