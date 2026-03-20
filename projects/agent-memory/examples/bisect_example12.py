"""
Memory bisect_example12
bisect_example12
"""
import bisect


def demo():
    a = [1, 3, 5, 7, 9]
    idx = bisect.bisect_right(a, 5)
    print(idx)


if __name__ == "__main__":
    demo()
