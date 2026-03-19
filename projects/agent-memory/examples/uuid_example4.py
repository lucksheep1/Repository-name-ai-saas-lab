"""
Memory uuid_example4
uuid_example4
"""
import uuid


def demo():
    ns = uuid.NAMESPACE_DNS
    name = "example.com"
    print(uuid.uuid3(ns, name))


if __name__ == "__main__":
    demo()
