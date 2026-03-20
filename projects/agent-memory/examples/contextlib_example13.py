"""
Memory contextlib_example13
contextlib_example13
"""
from contextlib import closing
import urllib.request


def demo():
    with closing(urllib.request.urlopen("https://httpbin.org/get")) as response:
        print(response.status)


if __name__ == "__main__":
    demo()
