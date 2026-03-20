"""
Memory marshal_example10
marshal_example10
"""
import marshal


def demo():
    data = marshal.dumps(42)
    print(marshal.loads(data))


if __name__ == "__main__":
    demo()
