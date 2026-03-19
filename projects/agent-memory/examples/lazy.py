"""
Memory Lazy
Lazy evaluation
"""
from memory import Memory


class Lazy:
    def __init__(self, func):
        self.func = func
        self.value = None
        self.evaluated = False
    
    def get(self):
        if not self.evaluated:
            self.value = self.func()
            self.evaluated = True
        return self.value


def demo():
    print("Lazy ready")


if __name__ == "__main__":
    demo()
