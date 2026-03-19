"""
Memory Map
Map over memories
"""
from memory import Memory


class Mapper:
    @staticmethod
    def map_content(memory, func):
        results = []
        for mem in memory.get_all():
            results.append(func(mem.get("content", "")))
        return results


def demo():
    print("Mapper ready")


if __name__ == "__main__":
    demo()
