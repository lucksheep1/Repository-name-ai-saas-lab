"""
Memory Migration
Migrate between storage backends
"""
from agent_memory import Memory


class MemoryMigrator:
    """Migrate memory between backends"""
    
    def __init__(self, source: Memory):
        self.source = source
    
    def migrate_to_json(self, path: str) -> int:
        """Migrate to JSON storage"""
        target = Memory(storage="json", path=path)
        
        count = 0
        for mem in self.source.get_all():
            target.add(
                content=mem.get("content", ""),
                tags=mem.get("tags", []),
                metadata=mem.get("metadata", {}),
                priority=mem.get("priority")
            )
            count += 1
        
        return count
    
    def migrate_to_sqlite(self, path: str) -> int:
        """Migrate to SQLite storage"""
        target = Memory(storage="sqlite", path=path)
        
        count = 0
        for mem in self.source.get_all():
            target.add(
                content=mem.get("content", ""),
                tags=mem.get("tags", []),
                metadata=mem.get("metadata", {}),
                priority=mem.get("priority")
            )
            count += 1
        
        return count
    
    def backup(self, path: str) -> int:
        """Backup to JSON"""
        return self.migrate_to_json(path)


def demo():
    """Demo migration"""
    # Source
    source = Memory(storage="json", path="./source.json")
    source.add("Memory 1")
    source.add("Memory 2")
    source.add("Memory 3", tags=["test"])
    
    print("=== Migration Demo ===\n")
    print(f"Source: {len(source.get_all())} memories")
    
    # Migrate
    migrator = MemoryMigrator(source)
    count = migrator.migrate_to_json("./target.json")
    print(f"Migrated: {count} memories")
    
    # Verify
    target = Memory(storage="json", path="./target.json")
    print(f"Target: {len(target.get_all())} memories")
    
    # Cleanup
    import os
    for f in ["./source.json", "./target.json"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    demo()
