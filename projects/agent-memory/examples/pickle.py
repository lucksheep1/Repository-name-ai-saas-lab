"""
Memory Pickle
Pickle support
"""
from memory import Memory
import pickle


def demo():
    data = {"test": 123}
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    print(unpickled)


if __name__ == "__main__":
    demo()
