"""
Memory Watcher
Watch for memory changes
"""
from agent_memory import Memory
import time


class MemoryWatcher:
    """Watch memory for changes"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.watchers = []  # [(pattern, callback)]
        self.last_snapshot = {}
        self.running = False
    
    def watch(self, pattern: str, callback: callable):
        """Watch for pattern"""
        self.watchers.append((pattern, callback))
    
    def check_changes(self):
        """Check for changes"""
        current = {m["id"]: m.get("content", "") for m in self.memory.get_all()}
        
        # Find new
        for mem_id, content in current.items():
            if mem_id not in self.last_snapshot:
                for pattern, callback in self.watchers:
                    if pattern in content:
                        callback("added", mem_id, content)
        
        # Find removed
        for mem_id in self.last_snapshot:
            if mem_id not in current:
                for pattern, callback in self.watchers:
                    callback("removed", mem_id, self.last_snapshot[mem_id])
        
        self.last_snapshot = current
    
    def watch_loop(self, interval: float = 1.0):
        """Watch loop"""
        self.running = True
        
        while self.running:
            self.check_changes()
            time.sleep(interval)
    
    def start_daemon(self, interval: float = 1.0):
        """Start watching in background"""
        import threading
        thread = threading.Thread(target=self.watch_loop, args=(interval,), daemon=True)
        thread.start()
    
    def stop(self):
        """Stop watching"""
        self.running = False


def demo():
    """Demo watcher"""
    memory = Memory(storage="json", path="./watch_demo.json")
    watcher = MemoryWatcher(memory)
    
    print("=== Memory Watcher Demo ===\n")
    
    # Watch for patterns
    watcher.watch("error", lambda action, id, content: 
        print(f"🚨 {action}: {content[:30]}"))
    
    watcher.watch("important", lambda action, id, content:
        print(f"⭐ {action}: {content[:30]}"))
    
    # Start watching
    watcher.start_daemon(interval=0.5)
    
    # Add memories (watcher will detect)
    memory.add("Normal operation")
    time.sleep(0.2)
    memory.add("Error occurred in system")
    time.sleep(0.2)
    memory.add("Important note")
    
    # Wait for detection
    time.sleep(1)
    
    watcher.stop()
    print("\nWatcher stopped")
    
    # Cleanup
    import os
    if os.path.exists("./watch_demo.json"):
        os.remove("./watch_demo.json")


if __name__ == "__main__":
    demo()
