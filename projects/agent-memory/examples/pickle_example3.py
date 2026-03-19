"""
Memory pickle_example3
pickle_example3
"""
import pickle


class Foo:
    def __init__(self, x):
        self.x = x


def demo():
    foo = Foo(42)
    data = pickle.dumps(foo)
    restored = pickle.loads(data)
    print(restored.x)


if __name__ == "__main__":
    demo()
