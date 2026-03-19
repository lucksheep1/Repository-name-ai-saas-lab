"""
Memory pickle_example6
pickle_example6
"""
import pickle


def demo():
    data = {"key": [1, 2, 3]}
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    print(unpickled == data)


if __name__ == "__main__":
    demo()
