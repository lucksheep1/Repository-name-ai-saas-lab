"""
Memory pprint_example3
pprint_example3
"""
from pprint import pprint


def demo():
    data = {"key" + str(i): {"nested": i} for i in range(3)}
    pprint(data)


if __name__ == "__main__":
    demo()
