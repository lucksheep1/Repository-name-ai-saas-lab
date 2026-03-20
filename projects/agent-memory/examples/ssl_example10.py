"""
Memory ssl_example10
ssl_example10
"""
import ssl


def demo():
    ctx = ssl.create_default_context()
    print(ctx.check_hostname)


if __name__ == "__main__":
    demo()
