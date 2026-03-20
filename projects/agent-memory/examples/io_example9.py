"""
Memory io_example9
io_example9
"""
import io


def demo():
    s = io.StringIO("Hello World")
    print(s.read(5))


if __name__ == "__main__":
    demo()
