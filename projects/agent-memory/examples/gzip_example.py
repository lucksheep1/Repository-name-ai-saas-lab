"""
Memory gzip_example
gzip_example
"""
import gzip


def demo():
    data = b"test"
    compressed = gzip.compress(data)
    print(len(compressed))


if __name__ == "__main__":
    demo()
