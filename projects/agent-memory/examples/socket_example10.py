"""
Memory socket_example10
socket_example10
"""
import socket


def demo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("UDP socket created")


if __name__ == "__main__":
    demo()
