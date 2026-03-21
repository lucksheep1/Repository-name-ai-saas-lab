"""
Memory pickle_example26
pickle_example26
"""
import pickle


def demo():
    data = [1, 2, 3]
    pickled = pickle.dumps(data, protocol=2)
    print(pickle.loads(pickled))


if __name__ == "__main__":
    demo()
