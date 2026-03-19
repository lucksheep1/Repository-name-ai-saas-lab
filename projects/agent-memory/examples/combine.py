"""
Memory Combine
Combine memories
"""
from memory import Memory


class Combine:
    @staticmethod
    def merge(mem1, mem2):
        combined = Memory(storage="json", path="merged.json")
        
        for mem in mem1.get_all():
            combined.add(mem.get("content", ""), tags=mem.get("tags", []))
        
        for mem in mem2.get_all():
            combined.add(mem.get("content", ""), tags=mem.get("tags", []))
        
        return combined


def demo():
    print("Combine ready")


if __name__ == "__main__":
    demo()
