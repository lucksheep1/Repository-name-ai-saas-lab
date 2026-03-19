"""
Memory pprint_example2
pprint_example2
"""
from pprint import pprint


def demo():
    data = {"key" + str(i): i for i in range(5)}
    pprint(data)


if __name__ == "__main__":
    demo()
