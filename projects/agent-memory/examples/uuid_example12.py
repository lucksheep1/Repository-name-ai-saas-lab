"""
Memory uuid_example12
uuid_example12
"""
import uuid


def demo():
    namespace = uuid.NAMESPACE_DNS
    name = "example.com"
    print(uuid.uuid3(namespace, name))


if __name__ == "__main__":
    demo()
