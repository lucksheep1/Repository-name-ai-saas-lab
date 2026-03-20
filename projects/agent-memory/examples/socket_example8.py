"""
Memory socket_example8
socket_example8
"""
import socket


def demo():
    print(socket.getaddrinfo("localhost", 8080))


if __name__ == "__main__":
    demo()
