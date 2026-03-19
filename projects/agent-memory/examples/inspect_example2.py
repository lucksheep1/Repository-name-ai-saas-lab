"""
Memory inspect_example2
inspect_example2
"""
import inspect


def demo():
    print(inspect.getsource(inspect.signature))


if __name__ == "__main__":
    demo()
