"""
Memory tempfile_example9
tempfile_example9
"""
import tempfile


def demo():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test")
        print(f.name)


if __name__ == "__main__":
    demo()
