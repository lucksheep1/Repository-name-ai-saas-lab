"""
Memory gzip
gzip utilities
"""
from memory import Memory
import gzip


def demo():
    data = b"test data"
    compressed = gzip.compress(data)
    decompressed = gzip.decompress(compressed)
    print(decompressed)


if __name__ == "__main__":
    demo()
