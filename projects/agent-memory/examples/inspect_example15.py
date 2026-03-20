"""
Memory inspect_example15
inspect_example15
"""
import inspect


def demo():
    print(inspect.getdoc(print))


if __name__ == "__main__":
    demo()
