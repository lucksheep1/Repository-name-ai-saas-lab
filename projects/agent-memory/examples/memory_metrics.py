"""
Memory Metrics
Metrics and monitoring
"""
from agent_memory import Memory


class MemoryMetrics:
    """Memory metrics"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.metrics = {
            "adds": 0,
            "searches": 0,
            "deletes": 0,
        }
    
    def record_add(self):
        """Record add"""
        self.metrics["adds"] += 1
    
    def record_search(self):
        """Record search"""
        self.metrics["searches"] += 1
    
    def record_delete(self):
        """Record delete"""
        self.metrics["deletes"] += 1
    
    def get_metrics(self):
        """Get metrics"""
        return {
            **self.metrics,
            "total_memories": len(self.memory.get_all())
        }


def demo():
    """Demo metrics"""
    memory = Memory(storage="json", path="./metrics_demo.json")
    metrics = MemoryMetrics(memory)
    
    memory.add("Test")
    metrics.record_add()
    
    print(f"Metrics: {metrics.get_metrics()}")


if __name__ == "__main__":
    demo()
