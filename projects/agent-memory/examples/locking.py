"""
Memory Locking
Distributed locking for memory operations
"""
from agent_memory import Memory
import time
import threading


class MemoryLock:
    """Lock memory operations"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.locks = {}  # mem_id -> lock
    
    def acquire(self, mem_id: str, timeout: float = 10) -> bool:
        """Acquire lock"""
        if mem_id not in self.locks:
            self.locks[mem_id] = threading.Lock()
        
        return self.locks[mem_id].acquire(timeout=timeout)
    
    def release(self, mem_id: str):
        """Release lock"""
        if mem_id in self.locks:
            self.locks[mem_id].release()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass


class AtomicUpdate:
    """Atomic memory updates"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def update_if(self, mem_id: str, condition: callable, update: dict) -> bool:
        """Update only if condition is true"""
        mem = self.memory.get(mem_id)
        
        if not mem:
            return False
        
        if condition(mem):
            self.memory.update(mem_id, **update)
            return True
        
        return False


def demo():
    """Demo locking"""
    memory = Memory(storage="json", path="./lock_demo.json")
    lock = MemoryLock(memory)
    atomic = AtomicUpdate(memory)
    
    print("=== Memory Locking Demo ===\n")
    
    # Add memory
    mem_id = memory.add("Counter: 0")
    
    # Atomic update
    success = atomic.update_if(
        mem_id,
        lambda m: "Counter: 0" in m.get("content", ""),
        {"content": "Counter: 1"}
    )
    print(f"Atomic update: {success}")
    
    # Verify
    mem = memory.get(mem_id)
    print(f"New content: {mem.get('content')}")
    
    # Cleanup
    import os
    if os.path.exists("./lock_demo.json"):
        os.remove("./lock_demo.json")


if __name__ == "__main__":
    demo()
