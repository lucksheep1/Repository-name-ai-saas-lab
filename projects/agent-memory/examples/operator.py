"""
Memory Operator
Operator utilities
"""
from memory import Memory
import operator


def demo():
    print(operator.add(1, 2))
    print(operator.mul(3, 4))
    print(operator.getitem([1, 2, 3], 1))


if __name__ == "__main__":
    demo()
