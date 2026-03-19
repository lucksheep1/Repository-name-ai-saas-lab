"""
Memory array_example
array_example
"""
from array import array


def demo():
    arr = array("i", [1, 2, 3])
    print(arr[0], arr[-1])


if __name__ == "__main__":
    demo()
