"""
Memory multiprocessing_example16
multiprocessing_example16
"""
import multiprocessing


def worker():
    return "done"


def demo():
    with multiprocessing.Pool(2) as p:
        print(p.apply(worker))


if __name__ == "__main__":
    demo()
