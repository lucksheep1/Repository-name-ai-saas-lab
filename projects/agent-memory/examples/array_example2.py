"""
Memory array_example2
array_example2
"""
import array


def demo():
    arr = array.array("i", [1, 2, 3])
    arr.append(4)
    print(len(arr))


if __name__ == "__main__":
    demo()
