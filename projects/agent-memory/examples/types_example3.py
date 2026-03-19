"""
Memory types_example3
types_example3
"""
import types


def demo():
    ns = types.SimpleNamespace(x=10, y=20)
    print(ns.x + ns.y)


if __name__ == "__main__":
    demo()
