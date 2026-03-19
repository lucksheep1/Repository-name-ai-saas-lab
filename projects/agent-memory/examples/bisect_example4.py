"""
Memory bisect_example4
bisect_example4
"""
import bisect


def demo():
    arr = [1, 3, 5, 7, 9]
    bisect.insort(arr, 4)
    print(arr)


if __name__ == "__main__":
    demo()
