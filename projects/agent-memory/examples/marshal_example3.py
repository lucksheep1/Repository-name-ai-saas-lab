"""
Memory marshal_example3
marshal_example3
"""
import marshal


def demo():
    data = {"key": "value"}
    marshalled = marshal.dumps(data)
    print(len(marshalled))


if __name__ == "__main__":
    demo()
