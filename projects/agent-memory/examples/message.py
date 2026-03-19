"""
Memory Message
WebSocket message
"""
from memory import Memory


async def on_message(ws, message):
    print(f"Received: {message}")


def demo():
    print("Message handler ready")


if __name__ == "__main__":
    demo()
