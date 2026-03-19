"""
Memory bisect_example5
bisect_example5
"""
import bisect


def demo():
    arr = [1, 2, 3, 4, 5]
    i = bisect.bisect_right(arr, 3)
    print(i)


if __name__ == "__main__":
    demo()
