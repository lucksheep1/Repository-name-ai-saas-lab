"""
Memory marshal_example7
marshal_example7
"""
import marshal


def demo():
    data = {"key": [1, 2, 3]}
    marshalled = marshal.dumps(data)
    print(len(marshalled))


if __name__ == "__main__":
    demo()
