"""
Memory marshal_example2
marshal_example2
"""
import marshal


def demo():
    code = compile("x = 1", "<string>", "exec")
    marshaled = marshal.dumps(code)
    unmarshaled = marshal.loads(marshaled)
    print(unmarshaled)


if __name__ == "__main__":
    demo()
