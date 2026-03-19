"""
Memory json_example6
json_example6
"""
import json


def demo():
    data = {"name": "test", "value": 123}
    json_str = json.dumps(data, separators=(",", ":"))
    print(json_str)


if __name__ == "__main__":
    demo()
