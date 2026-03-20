"""
Memory urllib_example9
urllib_example9
"""
import urllib.parse


def demo():
    params = {"key": "value", "foo": "bar"}
    query = urllib.parse.urlencode(params)
    print(query)


if __name__ == "__main__":
    demo()
