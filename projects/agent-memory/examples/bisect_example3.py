"""
Memory bisect_example3
bisect_example3
"""
import bisect


def demo():
    arr = [1, 2, 2, 2, 3]
    left = bisect.bisect_left(arr, 2)
    right = bisect.bisect_right(arr, 2)
    print(f"2 appears at positions {left} to {right-1}")


if __name__ == "__main__":
    demo()
