"""
Memory Snapshot
Snapshot pattern
"""
from memory import Memory
import json


class Snapshot:
    def __init__(self, state: list, timestamp: str):
        self.state = state
        self.timestamp = timestamp


class SnapshotMemory:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.snapshots = []
    
    def save_snapshot(self):
        from datetime import datetime
        state = self.memory.get_all()
        snapshot = Snapshot(state, datetime.now().isoformat())
        self.snapshots.append(snapshot)
    
    def restore(self, index: int = -1):
        if self.snapshots:
            snapshot = self.snapshots[index]
            
            for mem in self.memory.get_all():
                self.memory.forget(mem["id"])
            
            for item in snapshot.state:
                self.memory.add(
                    item.get("content", ""),
                    tags=item.get("tags", [])
                )


def demo():
    memory = Memory(storage="json", path="./snapshot_demo.json")
    sm = SnapshotMemory(memory)
    
    memory.add("Test1")
    sm.save_snapshot()
    
    memory.add("Test2")
    print(f"Before: {len(memory.get_all())}")
    
    sm.restore()
    print(f"After: {len(memory.get_all())}")


if __name__ == "__main__":
    demo()
