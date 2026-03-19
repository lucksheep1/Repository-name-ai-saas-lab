"""
Memory Final
Final constants
"""
from memory import Memory
from typing import final


class Base:
    @final
    def method(self):
        pass


def demo():
    print("Final ready")


if __name__ == "__main__":
    demo()
