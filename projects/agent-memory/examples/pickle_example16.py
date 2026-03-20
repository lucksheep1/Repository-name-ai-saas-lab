"""
Memory pickle_example16
pickle_example16
"""
import pickle


class Data:
    def __init__(self, value):
        self.value = value


def demo():
    d1 = Data([1, 2, 3])
    data = pickle.dumps(d1)
    d2 = pickle.loads(data)
    print(d2.value)


if __name__ == "__main__":
    demo()
