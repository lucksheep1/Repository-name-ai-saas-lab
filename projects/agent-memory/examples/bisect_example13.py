"""
Memory bisect_example13
bisect_example13
"""
import bisect


def demo():
    a = [1, 2, 3, 4, 5]
    print(bisect.bisect_left(a, 3))


if __name__ == "__main__":
    demo()
