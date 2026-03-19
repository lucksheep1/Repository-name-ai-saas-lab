"""
Memory urllib_example4
urllib_example4
"""
from urllib.parse import urljoin


def demo():
    print(urljoin("http://example.com/path/", "file.html"))


if __name__ == "__main__":
    demo()
