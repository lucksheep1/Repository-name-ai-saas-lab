"""
Memory Reduce
Reduce memories
"""
from memory import Memory


class Reduce:
    @staticmethod
    def count_by_tag(memory):
        from collections import Counter
        tags = []
        
        for mem in memory.get_all():
            tags.extend(mem.get("tags", []))
        
        return dict(Counter(tags))


def demo():
    print("Reduce ready")


if __name__ == "__main__":
    demo()
