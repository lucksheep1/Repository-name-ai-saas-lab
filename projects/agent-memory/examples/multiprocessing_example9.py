"""
Memory multiprocessing_example9
multiprocessing_example9
"""
import multiprocessing


def demo():
    m = multiprocessing.Manager()
    d = m.dict()
    d["key"] = "value"
    print(d["key"])


if __name__ == "__main__":
    demo()
