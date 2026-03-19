"""
Memory Lock
Thread-safe locking
"""
from memory import Memory
import threading


class Lock:
    def __init__(self):
        self.lock = threading.Lock()
    
    def __enter__(self):
        self.lock.acquire()
        return self
    
    def __exit__(self, *args):
        self.lock.release()


def demo():
    lock = Lock()
    with lock:
        print("Locked section")


if __name__ == "__main__":
    demo()
