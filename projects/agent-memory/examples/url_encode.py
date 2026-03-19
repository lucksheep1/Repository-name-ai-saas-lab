"""
Memory URL Encode
URL encoding
"""
from memory import Memory
from urllib.parse import quote, urlencode


def demo():
    encoded = quote("test=123&key=value")
    print(encoded)
    
    params = {"key": "value"}
    print(urlencode(params))


if __name__ == "__main__":
    demo()
