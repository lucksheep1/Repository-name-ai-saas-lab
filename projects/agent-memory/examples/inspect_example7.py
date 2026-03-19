"""
Memory inspect_example7
inspect_example7
"""
import inspect


def demo():
    def foo(a, b, c=1):
        pass
    sig = inspect.signature(foo)
    print(list(sig.parameters.keys()))


if __name__ == "__main__":
    demo()
