"""
Memory Serialization
Serialize/deserialize memory to various formats
"""
from agent_memory import Memory
import pickle
import base64
import json


class MemorySerializer:
    """Serialize memories"""
    
    def to_dict(self, memory: Memory) -> dict:
        """Serialize to dict"""
        return {
            "version": "1.0",
            "memories": memory.get_all()
        }
    
    def to_json(self, memory: Memory) -> str:
        """Serialize to JSON string"""
        return json.dumps(self.to_dict(memory), indent=2)
    
    def to_pickle(self, memory: Memory) -> bytes:
        """Serialize to pickle bytes"""
        return pickle.dumps(self.to_dict(memory))
    
    def to_base64(self, memory: Memory) -> str:
        """Serialize to base64 string"""
        return base64.b64encode(self.to_pickle(memory)).decode()
    
    def from_dict(self, data: dict, target: Memory) -> int:
        """Restore from dict"""
        memories = data.get("memories", [])
        
        imported = 0
        for mem in memories:
            target.add(
                content=mem.get("content", ""),
                tags=mem.get("tags", []),
                metadata=mem.get("metadata", {})
            )
            imported += 1
        
        return imported
    
    def from_json(self, json_str: str, target: Memory) -> int:
        """Restore from JSON"""
        data = json.loads(json_str)
        return self.from_dict(data, target)
    
    def from_pickle(self, data: bytes, target: Memory) -> int:
        """Restore from pickle"""
        data = pickle.loads(data)
        return self.from_dict(data, target)


def demo():
    """Demo serialization"""
    memory = Memory(storage="json", path="./serial_demo.json")
    
    print("=== Memory Serialization Demo ===\n")
    
    # Add memories
    memory.add("Test 1", tags=["a"])
    memory.add("Test 2", tags=["b"])
    
    # Serialize
    serializer = MemorySerializer()
    
    json_str = serializer.to_json(memory)
    print(f"JSON length: {len(json_str)} chars")
    
    b64 = serializer.to_base64(memory)
    print(f"Base64 length: {len(b64)} chars")
    
    # Restore to new memory
    new_memory = Memory(storage="json", path="./serial_restore.json")
    imported = serializer.from_json(json_str, new_memory)
    print(f"Restored: {imported} memories")
    
    # Cleanup
    import os
    for f in ["./serial_demo.json", "./serial_restore.json"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    demo()
