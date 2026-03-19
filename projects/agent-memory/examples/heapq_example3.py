"""
Memory heapq_example3
heapq_example3
"""
import heapq


def demo():
    data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
    heapq.heapify(data)
    largest = heapq.nlargest(3, data)
    print(largest)


if __name__ == "__main__":
    demo()
