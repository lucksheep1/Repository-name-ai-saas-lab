"""
Memory tempfile_example6
tempfile_example6
"""
import tempfile


def demo():
    with tempfile.TemporaryDirectory() as tmpdir:
        print(tmpdir)


if __name__ == "__main__":
    demo()
