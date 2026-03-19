"""
Memory pickle_example4
pickle_example4
"""
import pickle


def demo():
    data = [1, 2, {"key": "value"}]
    pickled = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    unpickled = pickle.loads(pickled)
    print(unpickled)


if __name__ == "__main__":
    demo()
