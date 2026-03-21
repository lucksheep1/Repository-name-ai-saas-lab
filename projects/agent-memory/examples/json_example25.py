"""
Memory json_example25
json_example25
"""
import json


def demo():
    data = {"name": "Alice", "age": 30}
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    demo()
