"""
Memory pickle_example20
pickle_example20
"""
import pickle


def demo():
    data = {"key": "value"}
    pickled = pickle.dumps(data)
    print(pickle.loads(pickled))


if __name__ == "__main__":
    demo()
