"""
Memory io_example9
io_example9
"""
import io


def demo():
    s = io.StringIO()
    s.write("Line 1\n")
    s.write("Line 2\n")
    s.seek(0)
    print(s.read())


if __name__ == "__main__":
    demo()
