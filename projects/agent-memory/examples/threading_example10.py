"""
Memory threading_example10
threading_example10
"""
import threading


def demo():
    barrier = threading.Barrier(2)
    print(barrier)


if __name__ == "__main__":
    demo()
