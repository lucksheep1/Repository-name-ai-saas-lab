"""
Memory types_example2
types_example2
"""
import types


def demo():
    ns = types.SimpleNamespace(x=1, y=2)
    print(ns.x, ns.y)


if __name__ == "__main__":
    demo()
