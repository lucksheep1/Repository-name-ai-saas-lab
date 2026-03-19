"""
Memory WebSocket
WebSocket wrapper
"""
from memory import Memory


class WebSocket:
    def __init__(self):
        self.connected = False
    
    async def connect(self, url):
        self.connected = True
    
    async def send(self, message):
        pass
    
    async def recv(self):
        return "message"
    
    async def close(self):
        self.connected = False


def demo():
    print("WebSocket ready")


if __name__ == "__main__":
    demo()
