"""
Memory time_example2
time_example2
"""
import time


def demo():
    start = time.time()
    time.sleep(0.01)
    elapsed = time.time() - start
    print(elapsed)


if __name__ == "__main__":
    demo()
