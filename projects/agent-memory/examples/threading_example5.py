"""
Memory threading_example5
threading_example5
"""
import threading


def demo():
    barrier = threading.Barrier(2)
    print(barrier)


if __name__ == "__main__":
    demo()
