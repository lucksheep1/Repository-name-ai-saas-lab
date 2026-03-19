"""
Memory Close
WebSocket close
"""
from memory import Memory


async def close(ws):
    await ws.close()


def demo():
    print("Close ready")


if __name__ == "__main__":
    demo()
