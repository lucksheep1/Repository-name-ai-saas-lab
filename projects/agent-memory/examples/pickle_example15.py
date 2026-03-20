"""
Memory pickle_example15
pickle_example15
"""
import pickle
import io


class MyData:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"MyData({self.value})"


def demo():
    data = MyData(42)
    serialized = pickle.dumps(data)
    deserialized = pickle.loads(serialized)
    print(deserialized)


if __name__ == "__main__":
    demo()
