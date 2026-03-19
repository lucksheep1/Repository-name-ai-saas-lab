"""
Memory Rate Limiter
Rate limit memory operations
"""
from agent_memory import Memory
import time


class RateLimiter:
    """Rate limit operations"""
    
    def __init__(self, max_calls: int, window: int):
        self.max_calls = max_calls
        self.window = window  # seconds
        self.calls = []
    
    def allow(self) -> bool:
        """Check if call is allowed"""
        now = time.time()
        
        # Remove old calls
        self.calls = [c for c in self.calls if now - c < self.window]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        
        return False
    
    def wait_time(self) -> float:
        """Get wait time until next allowed call"""
        if not self.calls:
            return 0
        
        now = time.time()
        oldest = min(self.calls)
        
        return max(0, self.window - (now - oldest))


class RateLimitedMemory:
    """Memory with rate limiting"""
    
    def __init__(self, memory: Memory, max_adds: int = 10, window: int = 60):
        self.memory = memory
        self.limiter = RateLimiter(max_adds, window)
    
    def add(self, content: str, **kwargs):
        """Add with rate limiting"""
        if not self.limiter.allow():
            wait = self.limiter.wait_time()
            raise Exception(f"Rate limited. Wait {wait:.1f}s")
        
        return self.memory.add(content, **kwargs)


def demo():
    """Demo rate limiter"""
    memory = Memory(storage="json", path="./rate_demo.json")
    limited = RateLimitedMemory(memory, max_adds=2, window=10)
    
    print("=== Rate Limiter Demo ===\n")
    
    # Try to add more than limit
    for i in range(5):
        try:
            limited.add(f"Message {i}")
            print(f"Added: Message {i}")
        except Exception as e:
            print(f"Rate limited: {e}")
    
    # Cleanup
    import os
    if os.path.exists("./rate_demo.json"):
        os.remove("./rate_demo.json")


if __name__ == "__main__":
    demo()
