"""
Memory pickle_example14
pickle_example14
"""
import pickle


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name}, {self.age}"


def demo():
    p = Person("Alice", 30)
    data = pickle.dumps(p)
    restored = pickle.loads(data)
    print(restored)


if __name__ == "__main__":
    demo()
