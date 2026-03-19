"""
Memory dis
dis utilities
"""
from memory import Memory
import dis


def demo():
    def foo():
        return 1
    dis.dis(foo)


if __name__ == "__main__":
    demo()
