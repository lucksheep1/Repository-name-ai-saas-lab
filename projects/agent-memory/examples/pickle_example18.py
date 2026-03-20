"""
Memory pickle_example18
pickle_example18
"""
import pickle


def demo():
    data = [1, 2, 3]
    pickled = pickle.dumps(data)
    print(pickle.loads(pickled))


if __name__ == "__main__":
    demo()
