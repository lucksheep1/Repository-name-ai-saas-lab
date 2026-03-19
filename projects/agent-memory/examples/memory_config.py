"""
Memory Config
Configuration for memory
"""
from memory import Memory


class Config:
    def __init__(self, data: dict = None):
        self.data = data or {}
    
    def get(self, key: str, default=None):
        return self.data.get(key, default)
    
    def set(self, key: str, value):
        self.data[key] = value
    
    def to_dict(self):
        return self.data


def demo():
    config = Config({"storage": "json", "path": "memory.json"})
    print(config.get("storage"))


if __name__ == "__main__":
    demo()
