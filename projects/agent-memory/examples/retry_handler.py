"""
Memory Retry Handler
Retry failed operations
"""
from agent_memory import Memory
import time


class RetryHandler:
    """Handle retries for memory operations"""
    
    def __init__(self, max_retries: int = 3, delay: float = 1.0):
        self.max_retries = max_retries
        self.delay = delay
    
    def retry_add(self, memory: Memory, content: str, **kwargs):
        """Retry add on failure"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return memory.add(content, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay)
        
        raise last_error
    
    def retry_search(self, memory: Memory, query: str, **kwargs):
        """Retry search on failure"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return memory.search(query, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay)
        
        raise last_error


class CircuitBreaker:
    """Circuit breaker for memory operations"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure = 0
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        """Call with circuit breaker"""
        if self.state == "open":
            # Check if should try half-open
            if time.time() - self.last_failure > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
            
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure = time.time()
            
            if self.failures >= self.failure_threshold:
                self.state = "open"
            
            raise


def demo():
    """Demo retry handler"""
    memory = Memory(storage="json", path="./retry_demo.json")
    retry = RetryHandler(max_retries=3, delay=0.5)
    
    print("=== Retry Handler Demo ===\n")
    
    # Add with retry
    mem_id = retry.retry_add(memory, "Test memory")
    print(f"Added with retry: {mem_id}")
    
    # Search with retry
    results = retry.retry_search(memory, "test")
    print(f"Found: {len(results)} results")
    
    # Circuit breaker demo
    cb = CircuitBreaker(failure_threshold=2, timeout=5)
    
    def failing_func():
        raise Exception("Simulated failure")
    
    for i in range(5):
        try:
            cb.call(failing_func)
        except Exception as e:
            print(f"Attempt {i+1}: {e}")
    
    print(f"\nCircuit breaker state: {cb.state}")
    
    # Cleanup
    import os
    if os.path.exists("./retry_demo.json"):
        os.remove("./retry_demo.json")


if __name__ == "__main__":
    demo()
