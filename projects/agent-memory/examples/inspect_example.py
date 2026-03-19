"""
Memory inspect_example
inspect_example
"""
import inspect


def demo():
    print(inspect.signature(print))


if __name__ == "__main__":
    demo()
