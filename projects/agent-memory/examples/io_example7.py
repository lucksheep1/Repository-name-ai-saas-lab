"""
Memory io_example7
io_example7
"""
import io


def demo():
    b = io.BytesIO(b"hello")
    print(b.getvalue())


if __name__ == "__main__":
    demo()
