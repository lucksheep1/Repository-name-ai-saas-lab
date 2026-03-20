"""
Memory pickle_example13
pickle_example13
"""
import pickle


def demo():
    data = {"key": "value", "list": [1, 2, 3], "nested": {"a": 1}}
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    print(len(unpickled))


if __name__ == "__main__":
    demo()
