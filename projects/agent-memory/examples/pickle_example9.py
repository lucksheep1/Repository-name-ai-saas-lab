"""
Memory pickle_example9
pickle_example9
"""
import pickle


def demo():
    data = {"key": "value", "list": [1, 2, 3]}
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    print(unpickled)


if __name__ == "__main__":
    demo()
