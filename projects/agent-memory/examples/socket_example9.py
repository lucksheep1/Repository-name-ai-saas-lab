"""
Memory socket_example9
socket_example9
"""
import socket


def demo():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    print(s.getsockname()[1])
    s.close()


if __name__ == "__main__":
    demo()
