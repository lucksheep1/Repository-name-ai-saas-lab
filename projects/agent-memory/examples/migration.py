"""
Memory Migration
Migrate between storage backends
"""
from agent_memory import Memory


class MemoryMigrator:
    """Migrate memory between backends"""
    
    def __init__(self, source: Memory):
        self.source = source
    
    def migrate_to(self, target_storage: str, target_path: str) -> int:
        """Migrate to new storage"""
        target = Memory(storage=target_storage, path=target_path)
        
        migrated = 0
        
        for mem in self.source.get_all():
            target.add(
                content=mem.get("content", ""),
                tags=mem.get("tags", []),
                metadata=mem.get("metadata", {})
            )
            migrated += 1
        
        return migrated
    
    def export_import(self, target_storage: str, target_path: str) -> int:
        """Export then import (for schema changes)"""
        # Export to JSON
        import json
        with open("./migration_temp.json", "w") as f:
            json.dump(self.source.get_all(), f)
        
        # Clear target
        target = Memory(storage=target_storage, path=target_path)
        
        # Import
        import json
        with open("./migration_temp.json", "r") as f:
            memories = json.load(f)
        
        migrated = 0
        for mem in memories:
            target.add(
                content=mem.get("content", ""),
                tags=mem.get("tags", []),
                metadata=mem.get("metadata", {})
            )
            migrated += 1
        
        # Cleanup
        import os
        os.remove("./migration_temp.json")
        
        return migrated


def demo():
    """Demo migration"""
    # Source
    source = Memory(storage="json", path="./source.json")
    source.add("Memory 1")
    source.add("Memory 2", tags=["test"])
    
    print("=== Memory Migration Demo ===\n")
    print(f"Source: {len(source.get_all())} memories")
    
    # Migrate
    migrator = MemoryMigrator(source)
    target_path = "./target.db"
    
    migrated = migrator.migrate_to("sqlite", target_path)
    print(f"Migrated: {migrated} memories")
    
    # Verify
    target = Memory(storage="sqlite", path=target_path)
    print(f"Target: {len(target.get_all())} memories")
    
    # Cleanup
    import os
    for f in ["./source.json", target_path]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    demo()
