"""
Memory Serialization
Serialize/deserialize memories
"""
from agent_memory import Memory
import pickle
import json


class MemorySerializer:
    """Serialize memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def to_dict(self) -> list:
        """Convert to dict"""
        return self.memory.get_all()
    
    def to_json(self, filepath: str = None) -> str:
        """Convert to JSON string"""
        data = self.to_dict()
        json_str = json.dumps(data, indent=2, default=str)
        
        if filepath:
            with open(filepath, "w") as f:
                f.write(json_str)
        
        return json_str
    
    def to_pickle(self, filepath: str = None) -> bytes:
        """Convert to pickle bytes"""
        data = self.to_dict()
        pickled = pickle.dumps(data)
        
        if filepath:
            with open(filepath, "wb") as f:
                f.write(pickled)
        
        return pickled
    
    def from_dict(self, data: list):
        """Load from dict"""
        for item in data:
            self.memory.add(
                content=item.get("content", ""),
                tags=item.get("tags", []),
                metadata=item.get("metadata", {}),
                priority=item.get("priority")
            )
    
    def from_json(self, json_str: str = None, filepath: str = None):
        """Load from JSON"""
        if filepath:
            with open(filepath, "r") as f:
                data = json.load(f)
        else:
            data = json.loads(json_str)
        
        self.from_dict(data)
    
    def from_pickle(self, pickled: bytes = None, filepath: str = None):
        """Load from pickle"""
        if filepath:
            with open(filepath, "rb") as f:
                data = pickle.load(f)
        else:
            data = pickle.loads(pickled)
        
        self.from_dict(data)


def demo():
    """Demo serialization"""
    source = Memory(storage="json", path="./serial_source.json")
    source.add("Memory 1")
    source.add("Memory 2", tags=["test"])
    
    print("=== Serialization Demo ===\n")
    
    # Serialize
    serializer = MemorySerializer(source)
    
    json_str = serializer.to_json()
    print(f"JSON: {json_str[:100]}...")
    
    # Save to file
    serializer.to_json("./serial_backup.json")
    print("Saved to serial_backup.json")
    
    # Load to new memory
    target = Memory(storage="json", path="./serial_target.json")
    loader = MemorySerializer(target)
    loader.from_json(filepath="./serial_backup.json")
    
    print(f"Loaded: {len(target.get_all())} memories")
    
    # Cleanup
    import os
    for f in ["./serial_source.json", "./serial_target.json", "./serial_backup.json"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    demo()
