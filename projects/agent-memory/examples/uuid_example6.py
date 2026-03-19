"""
Memory uuid_example6
uuid_example6
"""
import uuid


def demo():
    print(uuid.uuid4().hex[:16])


if __name__ == "__main__":
    demo()
