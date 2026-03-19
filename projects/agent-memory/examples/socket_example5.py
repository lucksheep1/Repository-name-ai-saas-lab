"""
Memory socket_example5
socket_example5
"""
import socket


def demo():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(s.type)


if __name__ == "__main__":
    demo()
