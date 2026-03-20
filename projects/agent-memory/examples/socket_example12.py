"""
Memory socket_example12
socket_example12
"""
import socket


def demo():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(s.family)


if __name__ == "__main__":
    demo()
