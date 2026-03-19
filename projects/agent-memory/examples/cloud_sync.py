"""
Memory Sync - Cloud Synchronization
Sync memories across multiple instances
"""
from agent_memory import Memory
import time
import threading


class MemorySync:
    """Sync memories across instances"""
    
    def __init__(self, memories: list):
        self.memories = memories  # List of Memory instances
        self.last_sync = {}
        self.running = False
    
    def sync_to(self, target: Memory) -> int:
        """Sync local memories to target"""
        synced = 0
        
        for mem in self.memories[0].get_all():
            # Check if exists in target
            existing = target.search(mem.get("content", "")[:50])
            
            if not existing:
                target.add(
                    content=mem.get("content", ""),
                    tags=mem.get("tags", []),
                    metadata={**mem.get("metadata", {}), "_synced": True}
                )
                synced += 1
        
        return synced
    
    def pull_from(self, source: Memory) -> int:
        """Pull from source"""
        synced = 0
        
        for mem in source.get_all():
            # Simple: add all
            self.memories[0].add(
                content=mem.get("content", ""),
                tags=mem.get("tags", []),
                metadata={**mem.get("metadata", {}), "_synced": True}
            )
            synced += 1
        
        return synced
    
    def sync_loop(self, interval: float = 60):
        """Background sync loop"""
        self.running = True
        
        while self.running:
            try:
                # Sync all memories to each other
                for i, mem in enumerate(self.memories):
                    for j, other in enumerate(self.memories):
                        if i != j:
                            self.sync_to(other)
            except Exception as e:
                print(f"Sync error: {e}")
            
            time.sleep(interval)
    
    def start_daemon(self, interval: float = 60):
        """Start background sync"""
        thread = threading.Thread(target=self.sync_loop, args=(interval,), daemon=True)
        thread.start()
    
    def stop(self):
        """Stop sync"""
        self.running = False


def demo():
    """Demo sync"""
    mem1 = Memory(storage="json", path="./sync1.json")
    mem2 = Memory(storage="json", path="./sync2.json")
    
    # Add to mem1
    mem1.add("Memory on device 1")
    mem1.add("Another memory")
    
    print("=== Memory Sync Demo ===\n")
    print(f"mem1: {len(mem1.get_all())} memories")
    print(f"mem2: {len(mem2.get_all())} memories")
    
    # Sync
    sync = MemorySync([mem1, mem2])
    synced = sync.sync_to(mem2)
    print(f"\nSynced {synced} memories to mem2")
    
    print(f"mem2 now: {len(mem2.get_all())} memories")
    
    # Cleanup
    import os
    for f in ["./sync1.json", "./sync2.json"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    demo()
