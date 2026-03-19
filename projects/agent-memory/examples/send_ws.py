"""
Memory Send
WebSocket send
"""
from memory import Memory


async def send(ws, message):
    await ws.send(message)


def demo():
    print("Send ready")


if __name__ == "__main__":
    demo()
