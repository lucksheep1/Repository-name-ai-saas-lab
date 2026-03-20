"""
Memory marshal_example4
marshal_example4
"""
import marshal


def demo():
    code = compile("x = 1", "<string>", "exec")
    marshalled = marshal.dumps(code)
    print(len(marshalled))


if __name__ == "__main__":
    demo()
