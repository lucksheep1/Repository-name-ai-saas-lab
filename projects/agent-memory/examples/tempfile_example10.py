"""
Memory tempfile_example10
tempfile_example10
"""
import tempfile
import os


def demo():
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Created: {tmpdir}")
        print(f"Exists: {os.path.exists(tmpdir)}")


if __name__ == "__main__":
    demo()
