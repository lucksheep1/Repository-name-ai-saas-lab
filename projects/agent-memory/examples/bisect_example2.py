"""
Memory bisect_example2
bisect_example2
"""
import bisect


def demo():
    arr = [1, 2, 3, 4, 5]
    bisect.insort(arr, 3.5)
    print(arr)


if __name__ == "__main__":
    demo()
