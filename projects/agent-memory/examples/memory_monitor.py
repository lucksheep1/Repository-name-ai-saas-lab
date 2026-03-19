"""
Memory Monitor
Monitor memory usage
"""
from memory import Memory


class Monitor:
    def __init__(self):
        self.stats = {"adds": 0, "searches": 0}
    
    def record_add(self):
        self.stats["adds"] += 1
    
    def record_search(self):
        self.stats["searches"] += 1
    
    def get_stats(self):
        return self.stats


def demo():
    monitor = Monitor()
    monitor.record_add()
    print(monitor.get_stats())


if __name__ == "__main__":
    demo()
