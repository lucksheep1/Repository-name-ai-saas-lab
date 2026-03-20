"""
Memory gzip_example11
gzip_example11
"""
import gzip


def demo():
    with gzip.open("file.gz", "wb") as f:
        f.write(b"test content")


if __name__ == "__main__":
    demo()
