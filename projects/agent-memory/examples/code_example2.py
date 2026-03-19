"""
Memory code_example2
code_example2
"""
import code


def demo():
    compiled = compile("x = 1", "<string>", "exec")
    print(compiled)


if __name__ == "__main__":
    demo()
