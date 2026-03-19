"""
Memory pickle
pickle utilities
"""
from memory import Memory
import pickle


def demo():
    data = {"key": "value"}
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    print(unpickled)


if __name__ == "__main__":
    demo()
