"""
Memory pickle_example10
pickle_example10
"""
import pickle


def demo():
    data = [1, 2, 3, {"key": "value"}]
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    print(unpickled)


if __name__ == "__main__":
    demo()
