"""
Memory Observer
Observer pattern for memory
"""
from memory import Memory


class Observer:
    """Observer"""
    def update(self, event: str, data: dict):
        pass


class Subject:
    """Subject"""
    def __init__(self):
        self.observers = []
    
    def attach(self, observer: Observer):
        self.observers.append(observer)
    
    def detach(self, observer: Observer):
        self.observers.remove(observer)
    
    def notify(self, event: str, data: dict):
        for obs in self.observers:
            obs.update(event, data)


class MemoryObserver(Observer):
    """Memory observer"""
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def update(self, event: str, data: dict):
        print(f"Event: {event}, Data: {data}")


def demo():
    """Demo observer"""
    memory = Memory(storage="json", path="./observer_demo.json")
    observer = MemoryObserver(memory)
    
    subject = Subject()
    subject.attach(observer)
    
    subject.notify("add", {"id": "1"})


if __name__ == "__main__":
    demo()
