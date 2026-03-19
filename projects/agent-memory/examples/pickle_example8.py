"""
Memory pickle_example8
pickle_example8
"""
import pickle


class Data:
    def __init__(self, value):
        self.value = value


def demo():
    d = Data(42)
    pickled = pickle.dumps(d)
    unpickled = pickle.loads(pickled)
    print(unpickled.value)


if __name__ == "__main__":
    demo()
