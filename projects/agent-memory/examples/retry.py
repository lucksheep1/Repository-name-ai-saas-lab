"""
Memory Retry Logic
Retry failed operations
"""
from agent_memory import Memory
import time


class RetryMemory:
    """Memory with retry logic"""
    
    def __init__(self, memory: Memory, max_retries: int = 3, backoff: float = 1.0):
        self.memory = memory
        self.max_retries = max_retries
        self.backoff = backoff
    
    def add_with_retry(self, content: str, **kwargs) -> str:
        """Add with retry"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return self.memory.add(content, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait = self.backoff * (2 ** attempt)
                    print(f"Retry {attempt+1} after {wait}s: {e}")
                    time.sleep(wait)
        
        raise last_error


class CircuitBreaker:
    """Circuit breaker for memory operations"""
    
    def __init__(self, memory: Memory, failure_threshold: int = 5):
        self.memory = memory
        self.failure_threshold = failure_threshold
        self.failures = 0
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        """Call with circuit breaker"""
        if self.state == "open":
            raise RuntimeError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
            
            return result
        
        except Exception as e:
            self.failures += 1
            
            if self.failures >= self.failure_threshold:
                self.state = "open"
                print("Circuit breaker OPENED")
            
            raise


def demo():
    """Demo retry"""
    memory = Memory(storage="json", path="./retry_demo.json")
    retry = RetryMemory(memory, max_retries=3, backoff=0.1)
    
    print("=== Retry Logic Demo ===\n")
    
    # Add with retry
    mem_id = retry.add_with_retry("Test memory")
    print(f"Added: {mem_id}")
    
    # Circuit breaker
    cb = CircuitBreaker(memory, failure_threshold=3)
    
    for i in range(5):
        try:
            cb.call(memory.add, f"Test {i}")
            print(f"Call {i+1}: success")
        except RuntimeError as e:
            print(f"Call {i+1}: {e}")
    
    print(f"Circuit state: {cb.state}")
    
    # Cleanup
    import os
    if os.path.exists("./retry_demo.json"):
        os.remove("./retry_demo.json")


if __name__ == "__main__":
    demo()
