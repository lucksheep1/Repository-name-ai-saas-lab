"""
Memory tempfile_example3
tempfile_example3
"""
import tempfile


def demo():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("Hello")
        print(f.name)


if __name__ == "__main__":
    demo()
