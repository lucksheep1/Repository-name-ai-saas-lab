"""
Memory threading_example19
threading_example19
"""
import threading


def demo():
    t = threading.current_thread()
    print(t.name)


if __name__ == "__main__":
    demo()
