"""
Memory json_example15
json_example15
"""
import json


def demo():
    data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
    print(json.dumps(data, sort_keys=True))


if __name__ == "__main__":
    demo()
