"""
Memory pickle_example25
pickle_example25
"""
import pickle


def demo():
    class Foo:
        def __init__(self, x):
            self.x = x
    
    f = Foo(42)
    pickled = pickle.dumps(f)
    loaded = pickle.loads(pickled)
    print(loaded.x)


if __name__ == "__main__":
    demo()
