"""
Memory io
io utilities
"""
import io


def demo():
    f = io.StringIO("hello")
    print(f.read())


if __name__ == "__main__":
    demo()
