"""
Memory pickle_example22
pickle_example22
"""
import pickle


def demo():
    data = {"a": 1}
    pickled = pickle.dumps(data)
    print(pickle.loads(pickled))


if __name__ == "__main__":
    demo()
