"""
Memory copy_example2
copy_example2
"""
import copy


def demo():
    original = {"a": 1, "b": [2, 3]}
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)
    print("copied")


if __name__ == "__main__":
    demo()
