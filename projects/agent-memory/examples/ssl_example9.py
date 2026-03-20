"""
Memory ssl_example9
ssl_example9
"""
import ssl


def demo():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    print(context.protocol)


if __name__ == "__main__":
    demo()
