"""
Memory Watcher
Watch for changes in memory
"""
from agent_memory import Memory
import time
import threading


class MemoryWatcher:
    """Watch memory for changes"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.last_state = {}
        self.callbacks = []
        self.running = False
    
    def start(self, interval: float = 1.0):
        """Start watching"""
        self.running = True
        self._capture_state()
        
        thread = threading.Thread(target=self._watch_loop, args=(interval,), daemon=True)
        thread.start()
    
    def stop(self):
        """Stop watching"""
        self.running = False
    
    def _capture_state(self):
        """Capture current state"""
        self.last_state = {}
        for mem in self.memory.get_all():
            self.last_state[mem["id"]] = mem
    
    def on_change(self, callback: callable):
        """Register callback"""
        self.callbacks.append(callback)
    
    def _watch_loop(self, interval: float):
        """Watch loop"""
        while self.running:
            try:
                self._check_changes()
            except:
                pass
            time.sleep(interval)
    
    def _check_changes(self):
        """Check for changes"""
        current = {}
        for mem in self.memory.get_all():
            current[mem["id"]] = mem
        
        # New memories
        for mem_id, mem in current.items():
            if mem_id not in self.last_state:
                self._trigger("add", mem)
        
        # Deleted memories
        for mem_id in self.last_state:
            if mem_id not in current:
                self._trigger("delete", self.last_state[mem_id])
        
        self.last_state = current
    
    def _trigger(self, event: str, mem: dict):
        """Trigger callbacks"""
        for callback in self.callbacks:
            try:
                callback(event, mem)
            except:
                pass


class MemoryHooks:
    """Hooks for memory events"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.hooks = {
            "pre_add": [],
            "post_add": [],
            "pre_search": [],
            "post_search": [],
        }
    
    def register(self, event: str, hook: callable):
        """Register hook"""
        if event in self.hooks:
            self.hooks[event].append(hook)
    
    def trigger(self, event: str, *args, **kwargs):
        """Trigger hooks"""
        for hook in self.hooks.get(event, []):
            hook(*args, **kwargs)


def demo():
    """Demo watcher"""
    memory = Memory(storage="json", path="./watcher_demo.json")
    watcher = MemoryWatcher(memory)
    
    print("=== Memory Watcher Demo ===\n")
    
    # Register callback
    def on_change(event, mem):
        print(f"Change: {event} - {mem.get('content', '')[:30]}")
    
    watcher.on_change(on_change)
    
    # Start watching
    watcher.start(interval=0.5)
    
    # Add memories
    time.sleep(0.2)
    memory.add("Memory 1")
    memory.add("Memory 2")
    
    time.sleep(1)
    
    # Stop
    watcher.stop()
    
    print("Done!")
    
    # Cleanup
    import os
    if os.path.exists("./watcher_demo.json"):
        os.remove("./watcher_demo.json")


if __name__ == "__main__":
    demo()
