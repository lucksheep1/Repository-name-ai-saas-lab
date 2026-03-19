"""
Memory ssl context
ssl context utilities
"""
import ssl


def demo():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    print(ctx)


if __name__ == "__main__":
    demo()
