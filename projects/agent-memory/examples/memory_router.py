"""
Memory Router
Route memory operations
"""
from memory import Memory


class Router:
    def __init__(self):
        self.routes = {}
    
    def register(self, path: str, handler):
        self.routes[path] = handler
    
    def route(self, path: str, *args):
        if path in self.routes:
            return self.routes[path](*args)
        return None


def demo():
    router = Router()
    
    def add_handler(content):
        return f"Added: {content}"
    
    router.register("add", add_handler)
    
    print(router.route("add", "Test"))


if __name__ == "__main__":
    demo()
