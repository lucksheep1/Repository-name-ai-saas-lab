"""
Memory DTO
Data Transfer Object for memory
"""
from memory import Memory


class MemoryDTO:
    def __init__(self, id: str, content: str, tags: list, created_at: str):
        self.id = id
        self.content = content
        self.tags = tags
        self.created_at = created_at
    
    @staticmethod
    def from_memory(mem: dict):
        return MemoryDTO(
            mem.get("id", ""),
            mem.get("content", ""),
            mem.get("tags", []),
            mem.get("created_at", "")
        )
    
    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at
        }


def demo():
    memory = Memory(storage="json", path="./dto_demo.json")
    memory.add("Test", tags=["demo"])
    
    mem = memory.get_all()[0]
    dto = MemoryDTO.from_memory(mem)
    
    print(f"DTO: {dto.content}")


if __name__ == "__main__":
    demo()
