"""
Memory marshal_example8
marshal_example8
"""
import marshal


def demo():
    code = compile("print('hello')", "<string>", "exec")
    marshalled = marshal.dumps(code)
    restored = marshal.loads(marshalled)
    exec(restored)


if __name__ == "__main__":
    demo()
