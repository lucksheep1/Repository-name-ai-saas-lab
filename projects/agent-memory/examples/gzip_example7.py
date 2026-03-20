"""
Memory gzip_example7
gzip_example7
"""
import gzip


def demo():
    with gzip.open("test.gz", "wb") as f:
        f.write(b"hello world")


if __name__ == "__main__":
    demo()
