"""
Memory Time Window
Time-windowed memory
"""
from agent_memory import Memory
from datetime import datetime, timedelta


class TimeWindow:
    """Time window"""
    
    def __init__(self, memory: Memory, window_hours: int = 24):
        self.memory = memory
        self.window = timedelta(hours=window_hours)
    
    def get_recent(self):
        """Get recent memories"""
        now = datetime.now()
        cutoff = now - self.window
        
        recent = []
        
        for mem in self.memory.get_all():
            created = datetime.fromisoformat(mem.get("created_at", now.isoformat()))
            
            if created >= cutoff:
                recent.append(mem)
        
        return recent
    
    def count_recent(self):
        """Count recent"""
        return len(self.get_recent())


def demo():
    """Demo time window"""
    memory = Memory(storage="json", path="./window_demo.json")
    tw = TimeWindow(memory, window_hours=24)
    
    memory.add("Test")
    
    print(f"Recent: {tw.count_recent()}")


if __name__ == "__main__":
    demo()
