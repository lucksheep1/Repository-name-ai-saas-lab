"""
Memory AsyncGen
Async generator
"""
from memory import Memory


async def async_gen(memory):
    for mem in memory.get_all():
        yield mem


def demo():
    print("Async gen ready")


if __name__ == "__main__":
    demo()
