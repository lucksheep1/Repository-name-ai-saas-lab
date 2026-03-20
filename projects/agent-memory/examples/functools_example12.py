"""
Memory functools_example12
functools_example12
"""
from functools import total_ordering


@total_ordering
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        return self.age == other.age
    
    def __lt__(self, other):
        return self.age < other.age


def demo():
    p1 = Person("Alice", 30)
    p2 = Person("Bob", 25)
    print(p1 > p2)


if __name__ == "__main__":
    demo()
