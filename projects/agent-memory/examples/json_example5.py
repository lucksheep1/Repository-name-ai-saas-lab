"""
Memory json_example5
json_example5
"""
import json


def demo():
    data = {"key": None, "bool": True, "num": 42}
    print(json.dumps(data))


if __name__ == "__main__":
    demo()
