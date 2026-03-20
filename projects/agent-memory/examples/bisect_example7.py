"""
Memory bisect_example7
bisect_example7
"""
import bisect


def demo():
    arr = [1, 2, 3, 4, 5]
    bisect.insort(arr, 3)
    print(arr)


if __name__ == "__main__":
    demo()
