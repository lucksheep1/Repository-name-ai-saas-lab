"""
Memory ClassVar
Class variable
"""
from memory import Memory
from typing import ClassVar


class MyClass:
    class_var: ClassVar[int] = 0
    
    def __init__(self):
        MyClass.class_var += 1


def demo():
    a = MyClass()
    b = MyClass()
    print(MyClass.class_var)


if __name__ == "__main__":
    demo()
