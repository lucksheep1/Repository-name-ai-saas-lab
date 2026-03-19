"""
Memory io_example3
io_example3
"""
import io


def demo():
    buf = io.BytesIO()
    buf.write(b"hello")
    buf.seek(0)
    print(buf.read())


if __name__ == "__main__":
    demo()
