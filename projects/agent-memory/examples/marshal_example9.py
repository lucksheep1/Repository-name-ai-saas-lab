"""
Memory marshal_example9
marshal_example9
"""
import marshal


def demo():
    data = marshal.dumps({"key": "value"})
    print(len(data))


if __name__ == "__main__":
    demo()
