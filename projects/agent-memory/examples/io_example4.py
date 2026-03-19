"""
Memory io_example4
io_example4
"""
import io


def demo():
    text_io = io.TextIOWrapper(io.BytesIO(b"hello"), encoding="utf-8")
    print(text_io.read())


if __name__ == "__main__":
    demo()
