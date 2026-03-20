"""
Memory io_example10
io_example10
"""
import io


def demo():
    b = io.BytesIO(b"binary data")
    print(b.read())


if __name__ == "__main__":
    demo()
