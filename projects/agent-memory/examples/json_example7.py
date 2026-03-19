"""
Memory json_example7
json_example7
"""
import json


def demo():
    data = {"key": None, "bool": False, "float": 3.14}
    print(json.dumps(data))


if __name__ == "__main__":
    demo()
