"""
Memory json_example13
json_example13
"""
import json


def demo():
    data = {"key": "value", "list": [1, 2, 3]}
    s = json.dumps(data)
    print(len(s))


if __name__ == "__main__":
    demo()
