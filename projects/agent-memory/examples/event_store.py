"""
Memory Event Store
Event sourcing with memory
"""
from agent_memory import Memory
from datetime import datetime


class EventStore:
    """Event store"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def append(self, event_type: str, data: dict):
        """Append event"""
        content = f"{event_type}: {data}"
        
        self.memory.add(
            content,
            tags=["event", event_type],
            metadata={"event_type": event_type, **data}
        )
    
    def get_events(self, event_type: str = None, limit: int = 100):
        """Get events"""
        if event_type:
            return self.memory.get_by_tag(event_type)
        
        return self.memory.get_all()[-limit:]
    
    def replay(self, from_time: str = None):
        """Replay events"""
        events = self.get_events()
        
        if from_time:
            from_ts = datetime.fromisoformat(from_time).timestamp()
            events = [e for e in events 
                     if datetime.fromisoformat(e.get("created_at")).timestamp() >= from_ts]
        
        return events


def demo():
    """Demo event store"""
    memory = Memory(storage="json", path="./event_demo2.json")
    store = EventStore(memory)
    
    store.append("user.created", {"user_id": "1"})
    store.append("user.updated", {"user_id": "1"})
    
    print("Events:", len(store.get_events()))
    
    import os
    if os.path.exists("./event_demo2.json"):
        os.remove("./event_demo2.json")


if __name__ == "__main__":
    demo()
