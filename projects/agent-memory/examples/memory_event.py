"""
Memory Event
Event handling
"""
from memory import Memory


class Event:
    def __init__(self, name: str, data: dict = None):
        self.name = name
        self.data = data or {}


class EventBus:
    def __init__(self):
        self.handlers = {}
    
    def subscribe(self, event: str, handler):
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)
    
    def publish(self, event: Event):
        for handler in self.handlers.get(event.name, []):
            handler(event)


def demo():
    bus = EventBus()
    bus.subscribe("add", lambda e: print(f"Added: {e.data}"))
    bus.publish(Event("add", {"content": "Test"}))


if __name__ == "__main__":
    demo()
