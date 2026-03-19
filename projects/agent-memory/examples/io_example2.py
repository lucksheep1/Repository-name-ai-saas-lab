"""
Memory io_example2
io_example2
"""
import io


def demo():
    buf = io.BytesIO(b"binary data")
    print(buf.getvalue())


if __name__ == "__main__":
    demo()
