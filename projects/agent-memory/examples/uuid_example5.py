"""
Memory uuid_example5
uuid_example5
"""
import uuid


def demo():
    print(uuid.uuid5(uuid.NAMESPACE_URL, "example.com"))


if __name__ == "__main__":
    demo()
