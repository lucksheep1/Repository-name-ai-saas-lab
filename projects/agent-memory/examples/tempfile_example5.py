"""
Memory tempfile_example5
tempfile_example5
"""
import tempfile


def demo():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        print(f.name)


if __name__ == "__main__":
    demo()
