"""
Memory Open Callback
Open callback
"""
from memory import Memory


async def on_open(ws):
    await ws.send("hello")


def demo():
    print("Open callback ready")


if __name__ == "__main__":
    demo()
