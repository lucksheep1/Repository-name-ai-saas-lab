"""
Memory Compressor
Compress memory data
"""
from memory import Memory


class Compressor:
    @staticmethod
    def compress(data: str) -> bytes:
        import zlib
        return zlib.compress(data.encode())
    
    @staticmethod
    def decompress(data: bytes) -> str:
        import zlib
        return zlib.decompress(data).decode()


def demo():
    text = "Hello World" * 100
    compressed = Compressor.compress(text)
    print(f"Original: {len(text)}, Compressed: {len(compressed)}")


if __name__ == "__main__":
    demo()
