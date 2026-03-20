"""
Memory io_example12
io_example12
"""
import io


def demo():
    b = io.BytesIO()
    b.write(b"hello")
    b.seek(0)
    print(b.read())


if __name__ == "__main__":
    demo()
