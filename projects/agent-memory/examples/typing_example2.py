"""
Memory typing_example2
typing_example2
"""
from typing import Optional, Union


def demo():
    x: Optional[int] = None
    y: Union[int, str] = 1
    print(x, y)


if __name__ == "__main__":
    demo()
