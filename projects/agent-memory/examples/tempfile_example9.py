"""
Memory tempfile_example9
tempfile_example9
"""
import tempfile


def demo():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")
        print(f.name)


if __name__ == "__main__":
    demo()
