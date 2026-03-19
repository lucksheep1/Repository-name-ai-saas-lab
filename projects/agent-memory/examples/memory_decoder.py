"""
Memory Decoder
Decode memory data
"""
from memory import Memory


class Decoder:
    @staticmethod
    def decode_json(data: str) -> dict:
        import json
        return json.loads(data)
    
    @staticmethod
    def decode_base64(data: str) -> str:
        import base64
        return base64.b64decode(data.encode()).decode()
    
    @staticmethod
    def decode_url(data: str) -> str:
        from urllib.parse import unquote
        return unquote(data)


def demo():
    import base64
    encoded = base64.b64encode(b"Hello").decode()
    print(f"Decoded: {Decoder.decode_base64(encoded)}")


if __name__ == "__main__":
    demo()
