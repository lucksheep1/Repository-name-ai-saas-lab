"""
Memory multiprocessing_example13
multiprocessing_example13
"""
import multiprocessing


def worker(q):
    q.put("result")


def demo():
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()
    print(q.get())
    p.join()


if __name__ == "__main__":
    demo()
