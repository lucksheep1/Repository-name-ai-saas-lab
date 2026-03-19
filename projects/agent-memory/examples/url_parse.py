"""
Memory URL Parse
URL parsing
"""
from memory import Memory
from urllib.parse import urlparse, parse_qs


def demo():
    url = "https://example.com/path?key=value"
    parsed = urlparse(url)
    print(parsed.scheme, parsed.netloc, parsed.path)
    print(parse_qs(parsed.query))


if __name__ == "__main__":
    demo()
