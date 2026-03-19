"""
Memory bisect_example
bisect_example
"""
import bisect


def demo():
    arr = [1, 2, 3, 4, 5]
    i = bisect.bisect_left(arr, 3)
    print(i)


if __name__ == "__main__":
    demo()
