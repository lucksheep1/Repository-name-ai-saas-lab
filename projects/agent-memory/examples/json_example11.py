"""
Memory json_example11
json_example11
"""
import json


def demo():
    data = {"key": "value"}
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    demo()
