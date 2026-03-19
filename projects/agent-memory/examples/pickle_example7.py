"""
Memory pickle_example7
pickle_example7
"""
import pickle


def demo():
    data = {"key": [1, 2, 3], "nested": {"a": 1}}
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    print(unpickled)


if __name__ == "__main__":
    demo()
