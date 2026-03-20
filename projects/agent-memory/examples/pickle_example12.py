"""
Memory pickle_example12
pickle_example12
"""
import pickle


def demo():
    print(pickle.loads(pickle.dumps({})))


if __name__ == "__main__":
    demo()
