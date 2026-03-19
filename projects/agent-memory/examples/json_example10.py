"""
Memory json_example10
json_example10
"""
import json


def demo():
    data = {"name": "Alice", "age": 30}
    print(json.dumps(data, separators=(",", ":")))


if __name__ == "__main__":
    demo()
