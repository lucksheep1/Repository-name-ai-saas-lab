"""
Memory copy_example
copy_example
"""
import copy


def demo():
    original = {"a": 1}
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)
    print(shallow, deep)


if __name__ == "__main__":
    demo()
