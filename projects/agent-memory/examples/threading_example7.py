"""
Memory threading_example7
threading_example7
"""
import threading


def demo():
    local = threading.local()
    local.value = 42
    print(local.value)


if __name__ == "__main__":
    demo()
