"""
Memory concurrent_example4
concurrent_example4
"""
from concurrent.futures import Future


def demo():
    f = Future()
    f.set_result("done")
    print(f.result())


if __name__ == "__main__":
    demo()
