"""
Memory Hooks
Lifecycle hooks for memories
"""
from agent_memory import Memory


class MemoryHooks:
    """Lifecycle hooks for memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.hooks = {
            "before_add": [],
            "after_add": [],
            "before_get": [],
            "after_get": [],
            "before_update": [],
            "after_update": [],
            "before_delete": [],
            "after_delete": [],
        }
    
    def register(self, event: str, callback: callable):
        """Register hook"""
        if event in self.hooks:
            self.hooks[event].append(callback)
    
    def trigger(self, event: str, *args, **kwargs):
        """Trigger hooks"""
        for callback in self.hooks.get(event, []):
            callback(*args, **kwargs)


class HookedMemory:
    """Memory with hooks"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.hooks = MemoryHooks(memory)
    
    def add(self, content: str, **kwargs):
        """Add with hooks"""
        self.hooks.trigger("before_add", content, kwargs)
        
        mem_id = self.memory.add(content, **kwargs)
        
        self.hooks.trigger("after_add", mem_id, content, kwargs)
        
        return mem_id
    
    def get(self, mem_id: str):
        """Get with hooks"""
        self.hooks.trigger("before_get", mem_id)
        
        mem = self.memory.get(mem_id)
        
        self.hooks.trigger("after_get", mem)
        
        return mem
    
    def update(self, mem_id: str, **updates):
        """Update with hooks"""
        self.hooks.trigger("before_update", mem_id, updates)
        
        result = self.memory.update(mem_id, **updates)
        
        self.hooks.trigger("after_update", mem_id, updates)
        
        return result
    
    def forget(self, mem_id: str):
        """Delete with hooks"""
        self.hooks.trigger("before_delete", mem_id)
        
        result = self.memory.forget(mem_id)
        
        self.hooks.trigger("after_delete", mem_id)
        
        return result


def demo():
    """Demo hooks"""
    memory = Memory(storage="json", path="./hook_demo.json")
    hooked = HookedMemory(memory)
    
    print("=== Memory Hooks Demo ===\n")
    
    # Register hooks
    hooked.hooks.register("after_add", lambda *a: print(f"  → Added!"))
    hooked.hooks.register("after_delete", lambda *a: print(f"  → Deleted!"))
    
    # Add (hooks will fire)
    print("Adding memories:")
    hooked.add("Test 1")
    hooked.add("Test 2")
    
    print("\nDeleting:")
    mem_id = memory.get_all()[0]["id"]
    hooked.forget(mem_id)
    
    print("\nDone")
    
    # Cleanup
    import os
    if os.path.exists("./hook_demo.json"):
        os.remove("./hook_demo.json")


if __name__ == "__main__":
    demo()
