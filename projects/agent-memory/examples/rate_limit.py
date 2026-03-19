"""
Memory Rate Limiting
Rate limit memory operations
"""
from agent_memory import Memory
import time


class RateLimiter:
    """Rate limit operations"""
    
    def __init__(self, max_calls: int, window: float):
        self.max_calls = max_calls
        self.window = window
        self.calls = []
    
    def allow(self) -> bool:
        """Check if call is allowed"""
        now = time.time()
        
        # Remove old calls
        self.calls = [t for t in self.calls if now - t < self.window]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        
        return False
    
    def wait_time(self) -> float:
        """Get wait time until next call"""
        if not self.calls:
            return 0
        
        now = time.time()
        oldest = min(self.calls)
        return max(0, self.window - (now - oldest))


class ThrottledMemory:
    """Memory with rate limiting"""
    
    def __init__(self, memory: Memory, max_adds_per_minute: int = 60):
        self.memory = memory
        self.add_limiter = RateLimiter(max_adds_per_minute, 60)
    
    def add(self, content: str, **kwargs) -> str:
        """Add with rate limiting"""
        if not self.add_limiter.allow():
            wait = self.add_limiter.wait_time()
            raise RuntimeError(f"Rate limited. Wait {wait:.1f}s")
        
        return self.memory.add(content, **kwargs)


def demo():
    """Demo rate limiting"""
    memory = Memory(storage="json", path="./rate_demo.json")
    throttled = ThrottledMemory(memory, max_adds_per_minute=5)
    
    print("=== Rate Limiting Demo ===\n")
    
    # Try to add many memories quickly
    for i in range(7):
        try:
            throttled.add(f"Memory {i}")
            print(f"Added memory {i}")
        except RuntimeError as e:
            print(f"Rate limited: {e}")
    
    # Cleanup
    import os
    if os.path.exists("./rate_demo.json"):
        os.remove("./rate_demo.json")


if __name__ == "__main__":
    demo()
