"""
Memory marshal_example
marshal_example
"""
import marshal


def demo():
    data = {"key": "value"}
    marshaled = marshal.dumps(data)
    unmarshaled = marshal.loads(marshaled)
    print(unmarshaled)


if __name__ == "__main__":
    demo()
