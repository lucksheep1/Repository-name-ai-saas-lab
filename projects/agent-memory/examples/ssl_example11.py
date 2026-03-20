"""
Memory ssl_example11
ssl_example11
"""
import ssl


def demo():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    print(ctx.verify_mode)


if __name__ == "__main__":
    demo()
