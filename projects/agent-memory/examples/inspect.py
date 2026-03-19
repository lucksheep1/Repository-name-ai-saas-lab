"""
Memory inspect
inspect utilities
"""
from memory import Memory
import inspect


def demo():
    print(inspect.signature(print))


if __name__ == "__main__":
    demo()
