"""
Memory Send
Send to task
"""
from memory import Memory
import asyncio


async def receiver():
    while True:
        try:
            value = await asyncio.get_event_loop().sock_recv(b"test")
            break
        except:
            pass
    print("got")


def demo():
    print("Send ready")


if __name__ == "__main__":
    demo()
