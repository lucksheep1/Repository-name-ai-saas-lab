"""
Memory json_example17
json_example17
"""
import json


def demo():
    data = {"key": "value"}
    print(json.dumps(data, separators=(",", ":")))


if __name__ == "__main__":
    demo()
