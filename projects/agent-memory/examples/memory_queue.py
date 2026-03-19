"""
Memory Queue
Queue-based memory operations
"""
from agent_memory import Memory
import queue
import threading


class MemoryQueue:
    """Queue for memory operations"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.q = queue.Queue()
        self.running = False
    
    def enqueue(self, operation: str, *args, **kwargs):
        """Enqueue operation"""
        self.q.put((operation, args, kwargs))
    
    def start(self):
        """Start processing"""
        self.running = True
        
        thread = threading.Thread(target=self._process, daemon=True)
        thread.start()
    
    def _process(self):
        """Process queue"""
        while self.running:
            try:
                op, args, kwargs = self.q.get(timeout=1)
                
                if op == "add":
                    self.memory.add(*args, **kwargs)
                elif op == "delete":
                    self.memory.forget(*args, **kwargs)
                
                self.q.task_done()
            except:
                pass
    
    def stop(self):
        """Stop"""
        self.running = False


def demo():
    """Demo queue"""
    memory = Memory(storage="json", path="./queue_demo.json")
    mq = MemoryQueue(memory)
    
    mq.start()
    mq.enqueue("add", "Test")
    
    import time
    time.sleep(0.5)
    
    print(f"Queue size: {mq.q.qsize()}")


if __name__ == "__main__":
    demo()
