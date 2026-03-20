"""
Memory io_example11
io_example11
"""
import io


def demo():
    b = io.BytesIO(b"hello")
    print(b.getvalue())


if __name__ == "__main__":
    demo()
