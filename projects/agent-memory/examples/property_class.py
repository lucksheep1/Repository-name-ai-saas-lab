"""
Memory Property Class
Property class
"""
from memory import Memory


class PropClass:
    def __init__(self):
        self._value = None
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self._value = val


def demo():
    p = PropClass()
    p.value = 10
    print(p.value)


if __name__ == "__main__":
    demo()
