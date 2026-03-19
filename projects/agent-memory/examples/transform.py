"""
Memory Transform
Transform memories
"""
from memory import Memory


class Transform:
    @staticmethod
    def uppercase(memory):
        for mem in memory.get_all():
            content = mem.get("content", "")
            memory.update(mem["id"], content=content.upper())


def demo():
    print("Transform ready")


if __name__ == "__main__":
    demo()
