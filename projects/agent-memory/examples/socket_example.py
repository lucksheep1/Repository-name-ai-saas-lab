"""
Memory socket_example
socket_example
"""
import socket


def demo():
    hostname = socket.gethostname()
    print(hostname)


if __name__ == "__main__":
    demo()
