"""
Memory io_example5
io_example5
"""
import io


def demo():
    b = io.BytesIO(b"hello")
    print(b.read())


if __name__ == "__main__":
    demo()
