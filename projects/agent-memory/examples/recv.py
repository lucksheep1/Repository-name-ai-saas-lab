"""
Memory Recv
WebSocket recv
"""
from memory import Memory


async def recv(ws):
    msg = await ws.recv()
    return msg


def demo():
    print("Recv ready")


if __name__ == "__main__":
    demo()
