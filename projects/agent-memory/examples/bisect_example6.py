"""
Memory bisect_example6
bisect_example6
"""
import bisect


def demo():
    arr = [1, 3, 5, 7, 9]
    i = bisect.bisect_left(arr, 4)
    print(i)


if __name__ == "__main__":
    demo()
