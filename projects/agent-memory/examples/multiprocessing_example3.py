"""
Memory multiprocessing_example3
multiprocessing_example3
"""
import multiprocessing


def worker(queue):
    queue.put("done")


def demo():
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()
    p.join()
    print(queue.get())


if __name__ == "__main__":
    demo()
