"""
Memory pickle_example23
pickle_example23
"""
import pickle


def demo():
    data = [1, 2, 3]
    pickled = pickle.dumps(data)
    print(pickle.loads(pickled))


if __name__ == "__main__":
    demo()
