"""
Memory multiprocessing_example5
multiprocessing_example5
"""
import multiprocessing


def worker(conn):
    conn.send("message from child")
    conn.close()


def demo():
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=worker, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()


if __name__ == "__main__":
    demo()
