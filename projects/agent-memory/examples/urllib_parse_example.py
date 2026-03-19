"""
Memory urllib_parse_example
urllib_parse_example
"""
from urllib.parse import urlparse, parse_qs


def demo():
    result = urlparse("https://example.com/path?a=1&b=2")
    print(result.hostname)


if __name__ == "__main__":
    demo()
