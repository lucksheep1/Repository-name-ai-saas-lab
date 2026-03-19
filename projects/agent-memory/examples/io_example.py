"""
Memory io_example
io_example
"""
import io


def demo():
    buf = io.StringIO("hello")
    print(buf.getvalue())


if __name__ == "__main__":
    demo()
