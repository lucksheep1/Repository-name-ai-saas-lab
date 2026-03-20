"""
Memory tempfile_example11
tempfile_example11
"""
import tempfile


def demo():
    with tempfile.SpooledTemporaryFile(max_size=1000) as f:
        f.write(b"test")
        f.seek(0)
        print(f.read())


if __name__ == "__main__":
    demo()
