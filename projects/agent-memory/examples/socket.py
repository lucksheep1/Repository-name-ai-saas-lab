"""
Memory socket
socket utilities
"""
import socket


def demo():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(s)


if __name__ == "__main__":
    demo()
