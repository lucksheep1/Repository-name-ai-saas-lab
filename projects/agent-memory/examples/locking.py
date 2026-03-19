"""
Memory Locking
Distributed locking for memory operations
"""
from agent_memory import Memory
import time
import threading


class MemoryLock:
    """Lock for memory operations"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.locks = {}
        self.lock = threading.Lock()
    
    def acquire(self, key: str, timeout: float = 10) -> bool:
        """Acquire lock"""
        start = time.time()
        
        while True:
            with self.lock:
                if key not in self.locks:
                    self.locks[key] = True
                    return True
            
            if time.time() - start > timeout:
                return False
            
            time.sleep(0.1)
    
    def release(self, key: str):
        """Release lock"""
        with self.lock:
            if key in self.locks:
                del self.locks[key]
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass


class LockedMemory:
    """Memory with locking"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.locker = MemoryLock(memory)
    
    def add_with_lock(self, content: str, lock_key: str = "default", **kwargs):
        """Add with lock"""
        if self.locker.acquire(lock_key):
            try:
                return self.memory.add(content, **kwargs)
            finally:
                self.locker.release(lock_key)
        else:
            raise Exception("Could not acquire lock")


def demo():
    """Demo locking"""
    memory = Memory(storage="json", path="./lock_demo.json")
    locked = LockedMemory(memory)
    
    print("=== Lock Demo ===\n")
    
    # Add with lock
    mem_id = locked.add_with_lock("Locked memory", lock_key="mykey")
    print(f"Added with lock: {mem_id}")
    
    # Cleanup
    import os
    if os.path.exists("./lock_demo.json"):
        os.remove("./lock_demo.json")


if __name__ == "__main__":
    demo()
