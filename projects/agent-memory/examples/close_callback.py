"""
Memory Close Callback
Close callback
"""
from memory import Memory


async def on_close(ws):
    print("Closed")


def demo():
    print("Close handler ready")


if __name__ == "__main__":
    demo()
