"""
Memory io_example6
io_example6
"""
import io


def demo():
    s = io.StringIO()
    s.write("hello")
    s.seek(0)
    print(s.read())


if __name__ == "__main__":
    demo()
