"""
Memory gzip_example2
gzip_example2
"""
import gzip


def demo():
    original = b"hello world" * 100
    compressed = gzip.compress(original)
    decompressed = gzip.decompress(compressed)
    print(len(compressed), len(decompressed))


if __name__ == "__main__":
    demo()
