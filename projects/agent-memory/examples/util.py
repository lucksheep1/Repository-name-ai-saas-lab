"""
Memory Util
Utilities
"""
from memory import Memory


def timestamp():
    from datetime import datetime
    return datetime.now().isoformat()


def uuid():
    import uuid
    return uuid.uuid4().hex


def demo():
    print(f"Time: {timestamp()}")
    print(f"UUID: {uuid()}")


if __name__ == "__main__":
    demo()
