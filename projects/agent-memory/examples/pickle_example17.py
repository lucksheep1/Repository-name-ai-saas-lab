"""
Memory pickle_example17
pickle_example17
"""
import pickle


def demo():
    data = {"a": 1, "b": 2}
    s = pickle.dumps(data)
    print(pickle.loads(s))


if __name__ == "__main__":
    demo()
