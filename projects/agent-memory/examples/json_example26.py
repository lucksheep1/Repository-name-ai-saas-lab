"""
Memory json_example26
json_example26
"""
import json


def demo():
    data = {"key": None, "list": [1, None, 3]}
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    demo()
