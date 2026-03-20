"""
Memory copy_example1
copy_example1
"""
import copy


def demo():
    original = [1, [2, 3], 4]
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)
    shallow[1].append(5)
    print(f"Original: {original}")
    print(f"Deep: {deep}")


if __name__ == "__main__":
    demo()
