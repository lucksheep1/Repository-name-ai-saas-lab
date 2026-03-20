"""
Memory json_example16
json_example16
"""
import json


def demo():
    data = {"float": 1.23, "int": 42, "bool": True}
    s = json.dumps(data)
    print(json.loads(s))


if __name__ == "__main__":
    demo()
