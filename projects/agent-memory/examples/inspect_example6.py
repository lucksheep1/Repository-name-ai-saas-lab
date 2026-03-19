"""
Memory inspect_example6
inspect_example6
"""
import inspect


def demo():
    class Foo:
        pass
    print(inspect.isclass(Foo))


if __name__ == "__main__":
    demo()
