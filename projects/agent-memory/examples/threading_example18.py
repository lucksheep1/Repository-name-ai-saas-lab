"""
Memory threading_example18
threading_example18
"""
import threading


def demo():
    print(threading.current_thread().name)


if __name__ == "__main__":
    demo()
