"""
Memory json_example9
json_example9
"""
import json


def demo():
    data = {"name": "test", "value": 123}
    s = json.dumps(data, sort_keys=True)
    print(s)


if __name__ == "__main__":
    demo()
