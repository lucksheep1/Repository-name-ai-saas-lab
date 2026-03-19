"""
Memory gzip_example3
gzip_example3
"""
import gzip


def demo():
    with gzip.open("test.txt.gz", "wt") as f:
        f.write("Hello, World!")
    with gzip.open("test.txt.gz", "rt") as f:
        print(f.read())


if __name__ == "__main__":
    demo()
