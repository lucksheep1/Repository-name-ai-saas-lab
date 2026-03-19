"""
Memory Fold
Fold memories
"""
from memory import Memory


class Folder:
    @staticmethod
    def fold(memory, func, initial=0):
        result = initial
        for mem in memory.get_all():
            result = func(result, len(mem.get("content", "")))
        return result


def demo():
    print("Folder ready")


if __name__ == "__main__":
    demo()
