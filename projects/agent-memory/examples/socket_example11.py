"""
Memory socket_example11
socket_example11
"""
import socket


def demo():
    s = socket.socket()
    s.bind(("localhost", 0))
    print(s.getsockname()[1])
    s.close()


if __name__ == "__main__":
    demo()
