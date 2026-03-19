"""
Memory Split
Split memories
"""
from memory import Memory


class Splitter:
    @staticmethod
    def split(memory, by_tag: str):
        matching = Memory(storage="json", path="matching.json")
        other = Memory(storage="json", path="other.json")
        
        for mem in memory.get_all():
            if by_tag in mem.get("tags", []):
                matching.add(mem.get("content", ""), tags=mem.get("tags", []))
            else:
                other.add(mem.get("content", ""), tags=mem.get("tags", []))
        
        return matching, other


def demo():
    print("Splitter ready")


if __name__ == "__main__":
    demo()
