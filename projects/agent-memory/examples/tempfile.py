"""
Memory tempfile
Tempfile utilities
"""
from memory import Memory
import tempfile


def demo():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        print(f.name)


if __name__ == "__main__":
    demo()
