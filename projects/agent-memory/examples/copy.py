"""
Memory copy
copy utilities
"""
from memory import Memory
import copy


def demo():
    original = {"a": 1, "b": [1, 2]}
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)
    print(shallow, deep)


if __name__ == "__main__":
    demo()
