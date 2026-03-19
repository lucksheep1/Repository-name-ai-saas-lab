"""
Memory JSON Decode
JSON decoder
"""
from memory import Memory
import json


class CustomDecoder(json.JSONDecoder):
    def decode(self, s):
        return super().decode(s)


def demo():
    data = '{"test": 123}'
    print(json.loads(data, cls=CustomDecoder))


if __name__ == "__main__":
    demo()
