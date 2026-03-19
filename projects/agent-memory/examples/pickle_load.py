"""
Memory Pickle Load
Pickle load
"""
from memory import Memory
import pickle


def demo():
    with open("data.pkl", "wb") as f:
        pickle.dump({"test": 123}, f)
    with open("data.pkl", "rb") as f:
        print(pickle.load(f))


if __name__ == "__main__":
    demo()
