"""
Memory array_example2
array_example2
"""
from array import array


def demo():
    arr = array("i", [10, 20, 30])
    arr.append(40)
    print(arr[-1])


if __name__ == "__main__":
    demo()
