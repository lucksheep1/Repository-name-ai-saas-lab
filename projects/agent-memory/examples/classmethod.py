"""
Memory Classmethod
Class method
"""
from memory import Memory


class ClassMemory:
    count = 0
    
    @classmethod
    def increment(cls):
        cls.count += 1
    
    @classmethod
    def get_count(cls):
        return cls.count


def demo():
    ClassMemory.increment()
    print(ClassMemory.get_count())


if __name__ == "__main__":
    demo()
