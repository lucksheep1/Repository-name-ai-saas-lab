"""
Memory operator_example4
operator_example4
"""
import operator


def demo():
    print(operator.attrgetter("__class__")(object))


if __name__ == "__main__":
    demo()
