"""
Memory bisect_example9
bisect_example9
"""
import bisect


def demo():
    a = [1, 2, 3, 4, 5]
    i = bisect.bisect_left(a, 3)
    print(i)


if __name__ == "__main__":
    demo()
