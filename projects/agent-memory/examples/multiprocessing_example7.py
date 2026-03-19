"""
Memory multiprocessing_example7
multiprocessing_example7
"""
import multiprocessing


def worker(q):
    q.put("done")


def demo():
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()
    print(q.get())
    p.join()


if __name__ == "__main__":
    demo()
