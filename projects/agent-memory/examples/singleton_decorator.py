"""
Memory Singleton
Singleton decorator
"""
from memory import Memory


def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class SingleMemory:
    def __init__(self):
        self.memory = Memory(storage="json", path="single.json")


def demo():
    s1 = SingleMemory()
    s2 = SingleMemory()
    print(s1 is s2)


if __name__ == "__main__":
    demo()
