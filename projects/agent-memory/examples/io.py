"""
Memory io
io utilities
"""
from memory import Memory
import io


def demo():
    buffer = io.StringIO()
    buffer.write("hello")
    print(buffer.getvalue())


if __name__ == "__main__":
    demo()
