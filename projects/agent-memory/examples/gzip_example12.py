"""
Memory gzip_example12
gzip_example12
"""
import gzip


def demo():
    with gzip.open("file.gz", "rt") as f:
        print(f.read()[:20])


if __name__ == "__main__":
    demo()
