"""
Memory pickle_example5
pickle_example5
"""
import pickle


def demo():
    class Foo:
        def __init__(self, x):
            self.x = x
    
    f = Foo(10)
    data = pickle.dumps(f)
    f2 = pickle.loads(data)
    print(f2.x)


if __name__ == "__main__":
    demo()
