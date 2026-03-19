"""
Memory json_example3
json_example3
"""
import json


def demo():
    data = {"key": "value", "num": 123}
    pretty = json.dumps(data, indent=2)
    print(pretty)


if __name__ == "__main__":
    demo()
