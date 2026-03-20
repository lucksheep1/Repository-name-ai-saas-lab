"""
Memory urllib_example6
urllib_example6
"""
import urllib.parse


def demo():
    params = urllib.parse.urlencode({"key": "value", "foo": "bar"})
    print(params)


if __name__ == "__main__":
    demo()
