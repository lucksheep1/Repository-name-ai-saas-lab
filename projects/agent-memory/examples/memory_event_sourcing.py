"""
Memory Event Sourcing
Event sourcing pattern
"""
from memory import Memory


class EventStore:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def append(self, event: dict):
        self.memory.add(
            f"Event: {event.get('type')}",
            tags=["event", event.get("type", "unknown")],
            metadata=event
        )
    
    def get_events(self, event_type: str = None):
        if event_type:
            return self.memory.get_by_tag(event_type)
        return self.memory.get_all()


class EventSource:
    def __init__(self, memory: Memory):
        self.events = EventStore(memory)
        self.state = {}
    
    def apply(self, event: dict):
        etype = event.get("type")
        
        if etype == "set":
            self.state[event.get("key")] = event.get("value")
        elif etype == "delete":
            self.state.pop(event.get("key"), None)
        
        self.events.append(event)
    
    def replay(self):
        for event in self.events.get_events():
            meta = event.get("metadata", {})
            self.apply(meta)


def demo():
    es = EventSource(Memory(storage="json", path="./es_demo.json"))
    
    es.apply({"type": "set", "key": "name", "value": "Test"})
    print(f"State: {es.state}")


if __name__ == "__main__":
    demo()
