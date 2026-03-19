"""
Memory Pipe
Pipe operations
"""
from memory import Memory


def pipe(value, *funcs):
    result = value
    for func in funcs:
        result = func(result)
    return result


def demo():
    result = pipe(5, lambda x: x + 1, lambda x: x * 2)
    print(result)


if __name__ == "__main__":
    demo()
