"""
Memory ssl_example
ssl_example
"""
import ssl


def demo():
    ctx = ssl.create_default_context()
    print(ctx)


if __name__ == "__main__":
    demo()
