"""
Memory Backup
Incremental backup
"""
from memory import Memory
import json


class IncrementalBackup:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.backups = []
    
    def backup(self):
        from datetime import datetime
        
        memories = self.memory.get_all()
        timestamp = datetime.now().isoformat()
        
        self.backups.append({
            "timestamp": timestamp,
            "count": len(memories),
            "data": memories
        })
        
        return timestamp
    
    def restore(self, timestamp: str = None):
        if timestamp:
            for b in self.backups:
                if b["timestamp"] == timestamp:
                    self._restore_data(b["data"])
                    return
        
        if self.backups:
            self._restore_data(self.backups[-1]["data"])
    
    def _restore_data(self, data: list):
        for mem in self.memory.get_all():
            self.memory.forget(mem["id"])
        
        for item in data:
            self.memory.add(
                item.get("content", ""),
                tags=item.get("tags", [])
            )


def demo():
    memory = Memory(storage="json", path="./backup_demo.json")
    backup = IncrementalBackup(memory)
    
    memory.add("Test1")
    backup.backup()
    
    memory.add("Test2")
    backup.restore()
    
    print(f"Count: {len(memory.get_all())}")


if __name__ == "__main__":
    demo()
