"""
Memory array_example1
array_example1
"""
import array


def demo():
    arr = array.array("i", [1, 2, 3, 4, 5])
    print(arr[2])
    arr.append(6)
    print(len(arr))


if __name__ == "__main__":
    demo()
