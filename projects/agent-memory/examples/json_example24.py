"""
Memory json_example24
json_example24
"""
import json


def demo():
    data = {"a": [1, 2, 3], "b": {"c": 1}}
    print(json.dumps(data))


if __name__ == "__main__":
    demo()
