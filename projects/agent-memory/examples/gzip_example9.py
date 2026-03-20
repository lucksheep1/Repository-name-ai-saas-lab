"""
Memory gzip_example9
gzip_example9
"""
import gzip


def demo():
    with gzip.open("file.txt.gz", "wt") as f:
        f.write("Hello World!")


if __name__ == "__main__":
    demo()
