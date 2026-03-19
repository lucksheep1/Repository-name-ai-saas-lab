"""
Memory Extension
Extension system
"""
from memory import Memory


class Extension:
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, *args, **kwargs):
        raise NotImplementedError


class ExtensionPoint:
    def __init__(self, name: str):
        self.name = name
        self.extensions = []
    
    def register(self, ext: Extension):
        self.extensions.append(ext)
    
    def run_all(self, *args, **kwargs):
        return [ext.execute(*args, **kwargs) for ext in self.extensions]


def demo():
    ep = ExtensionPoint("test")
    print("Extension point ready")


if __name__ == "__main__":
    demo()
