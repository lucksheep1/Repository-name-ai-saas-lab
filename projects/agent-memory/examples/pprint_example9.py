"""
Memory pprint_example9
pprint_example9
"""
import pprint


def demo():
    data = {"users": [{"id": i, "name": f"User{i}"} for i in range(3)]}
    pprint.pprint(data, width=40)


if __name__ == "__main__":
    demo()
