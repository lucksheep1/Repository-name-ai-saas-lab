"""
Memory ssl_example5
ssl_example5
"""
import ssl


def demo():
    ctx = ssl.create_default_context()
    print(ctx.protocol)


if __name__ == "__main__":
    demo()
