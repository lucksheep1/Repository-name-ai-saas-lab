"""
Memory Stream
Stream memory events
"""
from agent_memory import Memory


class MemoryStream:
    """Stream memory"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.listeners = []
    
    def add_listener(self, callback):
        """Add listener"""
        self.listeners.append(callback)
    
    def notify(self, event: str, data: dict):
        """Notify listeners"""
        for cb in self.listeners:
            cb(event, data)
    
    def add(self, content: str, **kwargs):
        """Add with notification"""
        mem_id = self.memory.add(content, **kwargs)
        
        self.notify("add", {"id": mem_id, "content": content})
        
        return mem_id


def demo():
    """Demo stream"""
    memory = Memory(storage="json", path="./stream_demo.json")
    stream = MemoryStream(memory)
    
    def listener(event, data):
        print(f"Event: {event}")
    
    stream.add_listener(listener)
    stream.add("Test")
    
    print("Stream demo done")


if __name__ == "__main__":
    demo()
