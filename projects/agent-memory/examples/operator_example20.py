"""
Memory operator_example20
operator_example20
"""
import operator


def demo():
    print(operator.attrgetter("x")(type("X", (), {"x": 42})()))


if __name__ == "__main__":
    demo()
