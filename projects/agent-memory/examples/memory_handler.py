"""
Memory Handler
Handler pattern
"""
from memory import Memory


class Handler:
    def __init__(self, next_handler=None):
        self.next = next_handler
    
    def handle(self, request):
        if self.next:
            return self.next.handle(request)


class AddHandler(Handler):
    def handle(self, request):
        if request["type"] == "add":
            return {"result": "added"}
        return super().handle(request)


def demo():
    handler = AddHandler()
    print(handler.handle({"type": "add"}))


if __name__ == "__main__":
    demo()
