"""
Memory threading_example9
threading_example9
"""
import threading


def demo():
    event = threading.Event()
    print(event.is_set())


if __name__ == "__main__":
    demo()
