"""
Memory pickle_example11
pickle_example11
"""
import pickle


def demo():
    data = {"key": [1, 2, 3]}
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    print(unpickled)


if __name__ == "__main__":
    demo()
