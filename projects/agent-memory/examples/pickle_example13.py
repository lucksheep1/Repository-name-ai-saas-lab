"""
Memory pickle_example13
pickle_example13
"""
import pickle


class Data:
    def __init__(self, value):
        self.value = value


def demo():
    d = Data(100)
    pickled = pickle.dumps(d)
    restored = pickle.loads(pickled)
    print(restored.value)


if __name__ == "__main__":
    demo()
