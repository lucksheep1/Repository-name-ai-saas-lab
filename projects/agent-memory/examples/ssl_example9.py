"""
Memory ssl_example9
ssl_example9
"""
import ssl


def demo():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    print(ctx)


if __name__ == "__main__":
    demo()
