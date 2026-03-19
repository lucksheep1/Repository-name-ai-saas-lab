"""
Memory Plugins
Extensible plugin system for memory
"""
from agent_memory import Memory
from typing import Dict, Any, Callable


class MemoryPlugin:
    """Base plugin class"""
    
    name = "base"
    version = "1.0"
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def on_add(self, mem_id: str, content: str, kwargs: dict):
        """Called when memory is added"""
        pass
    
    def on_search(self, results: list, query: str):
        """Called when search happens"""
        pass
    
    def on_get(self, mem: dict):
        """Called when memory is retrieved"""
        pass


class PluginManager:
    """Manage memory plugins"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.plugins: Dict[str, MemoryPlugin] = {}
    
    def register(self, plugin: MemoryPlugin):
        """Register a plugin"""
        self.plugins[plugin.name] = plugin
    
    def unregister(self, name: str):
        """Unregister a plugin"""
        if name in self.plugins:
            del self.plugins[name]
    
    def trigger_add(self, mem_id: str, content: str, kwargs: dict):
        """Trigger on_add for all plugins"""
        for plugin in self.plugins.values():
            plugin.on_add(mem_id, content, kwargs)
    
    def trigger_search(self, results: list, query: str):
        """Trigger on_search for all plugins"""
        for plugin in self.plugins.values():
            plugin.on_search(results, query)
    
    def trigger_get(self, mem: dict):
        """Trigger on_get for all plugins"""
        for plugin in self.plugins.values():
            plugin.on_get(mem)


# Example plugins
class LoggingPlugin(MemoryPlugin):
    """Log all memory operations"""
    name = "logging"
    
    def on_add(self, mem_id: str, content: str, kwargs: dict):
        print(f"📝 [{self.name}] Added: {content[:30]}...")


class AnalyticsPlugin(MemoryPlugin):
    """Track memory analytics"""
    name = "analytics"
    
    def __init__(self, memory):
        super().__init__(memory)
        self.stats = {"adds": 0, "searches": 0, "gets": 0}
    
    def on_add(self, mem_id: str, content: str, kwargs: dict):
        self.stats["adds"] += 1
    
    def on_search(self, results: list, query: str):
        self.stats["searches"] += 1
    
    def on_get(self, mem: dict):
        self.stats["gets"] += 1
    
    def get_stats(self):
        return self.stats


class FilterPlugin(MemoryPlugin):
    """Filter certain content"""
    name = "filter"
    
    def __init__(self, memory, blocked_words: list = None):
        super().__init__(memory)
        self.blocked_words = blocked_words or ["password", "secret", "token"]
    
    def on_add(self, mem_id: str, content: str, kwargs: dict):
        content_lower = content.lower()
        
        for word in self.blocked_words:
            if word in content_lower:
                print(f"🚫 [{self.name}] Blocked: contains '{word}'")
                self.memory.forget(mem_id)
                break


class HighlightPlugin(MemoryPlugin):
    """Highlight important memories"""
    name = "highlight"
    
    def on_add(self, mem_id: str, content: str, kwargs: dict):
        # Auto-highlight urgent/important
        if any(w in content.lower() for w in ["urgent", "important", "critical"]):
            print(f"⭐ [{self.name}] Highlighted: {content[:30]}...")


def demo():
    """Demo plugins"""
    memory = Memory(storage="json", path="./plugin_demo.json")
    manager = PluginManager(memory)
    
    print("=== Memory Plugins Demo ===\n")
    
    # Register plugins
    manager.register(LoggingPlugin(memory))
    analytics = AnalyticsPlugin(memory)
    manager.register(analytics)
    manager.register(FilterPlugin(memory))
    manager.register(HighlightPlugin(memory))
    
    # Add memories (plugins will trigger)
    print("Adding memories:\n")
    memory.add("Normal conversation")
    memory.add("Important meeting tomorrow")
    memory.add("Critical bug found")
    
    # Show analytics
    print(f"\nAnalytics: {analytics.get_stats()}")
    
    # Cleanup
    import os
    if os.path.exists("./plugin_demo.json"):
        os.remove("./plugin_demo.json")


if __name__ == "__main__":
    demo()
