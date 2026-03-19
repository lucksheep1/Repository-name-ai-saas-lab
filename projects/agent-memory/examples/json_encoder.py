"""
Memory JSON Encode
JSON encoder
"""
from memory import Memory
import json


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        return str(obj)


def demo():
    data = {"test": 123}
    print(json.dumps(data, cls=CustomEncoder))


if __name__ == "__main__":
    demo()
