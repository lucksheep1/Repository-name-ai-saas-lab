"""
Memory bisect_example10
bisect_example10
"""
import bisect


def demo():
    a = [1, 2, 3, 4, 5]
    bisect.insort(a, 3)
    print(a)


if __name__ == "__main__":
    demo()
