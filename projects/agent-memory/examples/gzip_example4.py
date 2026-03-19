"""
Memory gzip_example4
gzip_example4
"""
import gzip


def demo():
    with gzip.open("test.txt.gz", "wb") as f:
        f.write(b"test data")


if __name__ == "__main__":
    demo()
