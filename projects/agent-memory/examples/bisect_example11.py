"""
Memory bisect_example11
bisect_example11
"""
import bisect


def demo():
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    i = bisect.bisect_left(a, 7)
    print(f"Index: {i}")


if __name__ == "__main__":
    demo()
