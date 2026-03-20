"""
Memory gzip_example10
gzip_example10
"""
import gzip


def demo():
    with gzip.open("file.txt.gz", "rt") as f:
        print(f.read()[:50])


if __name__ == "__main__":
    demo()
