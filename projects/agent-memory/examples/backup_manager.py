"""
Memory Backup & Restore
Automated backup and point-in-time recovery
"""
from agent_memory import Memory
import shutil
import os
import json
from datetime import datetime


class BackupManager:
    """Manage memory backups"""
    
    def __init__(self, memory: Memory, backup_dir: str = "./backups"):
        self.memory = memory
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def backup(self, name: str = None) -> str:
        """Create a backup"""
        if name is None:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filepath = os.path.join(self.backup_dir, f"backup_{name}.json")
        
        memories = self.memory.get_all()
        
        with open(filepath, "w") as f:
            json.dump({
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "memories": memories
            }, f, indent=2)
        
        return filepath
    
    def restore(self, filepath: str) -> int:
        """Restore from backup"""
        with open(filepath, "r") as f:
            data = json.load(f)
        
        memories = data.get("memories", [])
        
        # Clear current and restore
        current = self.memory.get_all()
        for mem in current:
            self.memory.forget(mem["id"])
        
        # Add restored memories
        for mem in memories:
            self.memory.add(
                content=mem.get("content", ""),
                tags=mem.get("tags", []),
                metadata=mem.get("metadata", {}),
                priority=mem.get("priority")
            )
        
        return len(memories)
    
    def list_backups(self) -> list:
        """List all backups"""
        backups = []
        
        for f in os.listdir(self.backup_dir):
            if f.startswith("backup_") and f.endswith(".json"):
                path = os.path.join(self.backup_dir, f)
                size = os.path.getsize(path)
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                backups.append({
                    "name": f.replace("backup_", "").replace(".json", ""),
                    "path": path,
                    "size": size,
                    "mtime": mtime.isoformat()
                })
        
        return sorted(backups, key=lambda x: x["mtime"], reverse=True)
    
    def auto_backup(self, max_backups: int = 10):
        """Auto backup with rotation"""
        # Create new backup
        self.backup()
        
        # Rotate old backups
        backups = self.list_backups()
        
        if len(backups) > max_backups:
            for old in backups[max_backups:]:
                os.remove(old["path"])


def demo():
    """Demo backup"""
    memory = Memory(storage="json", path="./backup_demo.json")
    manager = BackupManager(memory, backup_dir="./demo_backups")
    
    print("=== Backup Manager Demo ===\n")
    
    # Add some memories
    memory.add("Memory 1")
    memory.add("Memory 2")
    memory.add("Memory 3")
    
    print("Added 3 memories")
    
    # Create backup
    path = manager.backup("test")
    print(f"Created backup: {path}")
    
    # Delete all memories
    for mem in memory.get_all():
        memory.forget(mem["id"])
    print("Deleted all memories")
    
    # Restore
    count = manager.restore(path)
    print(f"Restored {count} memories")
    
    # List backups
    backups = manager.list_backups()
    print(f"Backups: {len(backups)}")
    
    # Cleanup
    import shutil
    shutil.rmtree("./demo_backups", ignore_errors=True)
    if os.path.exists("./backup_demo.json"):
        os.remove("./backup_demo.json")


if __name__ == "__main__":
    demo()
