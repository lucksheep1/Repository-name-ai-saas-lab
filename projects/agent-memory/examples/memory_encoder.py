"""
Memory Encoder
Encode memory data
"""
from memory import Memory


class Encoder:
    @staticmethod
    def encode_json(data: dict) -> str:
        import json
        return json.dumps(data)
    
    @staticmethod
    def encode_base64(data: str) -> str:
        import base64
        return base64.b64encode(data.encode()).decode()
    
    @staticmethod
    def encode_url(data: str) -> str:
        from urllib.parse import quote
        return quote(data)


def demo():
    data = "Hello World"
    print(f"Base64: {Encoder.encode_base64(data)}")
    print(f"URL: {Encoder.encode_url(data)}")


if __name__ == "__main__":
    demo()
