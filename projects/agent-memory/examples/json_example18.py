"""
Memory json_example18
json_example18
"""
import json


def demo():
    data = {"key": "value", "num": 42}
    print(json.dumps(data, sort_keys=True))


if __name__ == "__main__":
    demo()
