"""
Memory Plugin
Plugin system
"""
from memory import Memory


class Plugin:
    def __init__(self, name: str):
        self.name = name
    
    def install(self, memory: Memory):
        pass
    
    def uninstall(self):
        pass


class PluginManager:
    def __init__(self):
        self.plugins = {}
    
    def register(self, plugin: Plugin):
        self.plugins[plugin.name] = plugin
    
    def unregister(self, name: str):
        if name in self.plugins:
            del self.plugins[name]


def demo():
    pm = PluginManager()
    print("Plugin system ready")


if __name__ == "__main__":
    demo()
