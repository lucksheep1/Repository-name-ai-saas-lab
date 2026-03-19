"""
Memory Mapper
Data mapper pattern
"""
from memory import Memory


class MemoryMapper:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def to_entity(self, data: dict) -> dict:
        return {
            "id": data.get("id"),
            "content": data.get("content"),
            "tags": data.get("tags", []),
            "created": data.get("created_at")
        }
    
    def to_data(self, entity: dict) -> dict:
        return {
            "content": entity.get("content"),
            "tags": entity.get("tags", []),
            "created_at": entity.get("created")
        }
    
    def insert(self, entity: dict):
        data = self.to_data(entity)
        return self.memory.add(**data)
    
    def find(self, mem_id: str):
        data = self.memory.get(mem_id)
        if data:
            return self.to_entity(data)
        return None


def demo():
    mapper = MemoryMapper(Memory(storage="json", path="./mapper_demo.json"))
    
    entity = {"content": "Test", "tags": ["demo"]}
    mapper.insert(entity)
    
    print(f"Found: {mapper.find(mapper.memory.get_all()[0]['id'])}")


if __name__ == "__main__":
    demo()
