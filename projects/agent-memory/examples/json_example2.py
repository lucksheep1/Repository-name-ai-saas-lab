"""
Memory json_example2
json_example2
"""
import json


def demo():
    data = {"key": "value", "list": [1, 2, 3]}
    json_str = json.dumps(data)
    parsed = json.loads(json_str)
    print(parsed)


if __name__ == "__main__":
    demo()
