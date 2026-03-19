"""
Memory Exception
Custom exceptions
"""
from memory import Memory


class MemoryError(Exception):
    pass


class NotFoundError(MemoryError):
    pass


class ValidationError(MemoryError):
    pass


def demo():
    try:
        raise NotFoundError("Not found")
    except MemoryError as e:
        print(f"Caught: {e}")


if __name__ == "__main__":
    demo()
