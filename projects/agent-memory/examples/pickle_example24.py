"""
Memory pickle_example24
pickle_example24
"""
import pickle


def demo():
    data = {"key": [1, 2, 3]}
    pickled = pickle.dumps(data)
    print(pickle.loads(pickled))


if __name__ == "__main__":
    demo()
