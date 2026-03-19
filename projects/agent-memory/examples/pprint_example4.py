"""
Memory pprint_example4
pprint_example4
"""
import pprint


def demo():
    data = {"key": [1, 2, 3], "nested": {"a": 1}}
    pprint.pprint(data)


if __name__ == "__main__":
    demo()
