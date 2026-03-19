"""
Memory User Preferences
Store and retrieve user preferences
"""
from agent_memory import Memory


class Preferences:
    """User preferences stored in memory"""
    
    def __init__(self, memory: Memory, user_id: str = "default"):
        self.memory = memory
        self.user_id = user_id
        self.prefix = f"pref:{user_id}:"
    
    def set(self, key: str, value):
        """Set preference"""
        content = f"{key}={value}"
        mem_id = f"{self.prefix}{key}"
        
        # Try to update existing
        existing = self.memory.search(key)
        
        for mem in existing:
            if key in mem.get("content", ""):
                self.memory.update(mem["id"], content=content)
                return mem["id"]
        
        # Add new
        return self.memory.add(content, tags=["preference", "user"])
    
    def get(self, key: str, default=None):
        """Get preference"""
        search_results = self.memory.search(key)
        
        for mem in search_results:
            content = mem.get("content", "")
            
            if content.startswith(f"{key}="):
                value = content.split("=", 1)[1]
                
                # Try to parse
                if value.lower() == "true":
                    return True
                elif value.lower() == "false":
                    return False
                elif value.isdigit():
                    return int(value)
                
                return value
        
        return default
    
    def get_all(self) -> dict:
        """Get all preferences"""
        prefs = {}
        
        for mem in self.memory.get_all():
            tags = mem.get("tags", [])
            
            if "preference" in tags and "user" in tags:
                content = mem.get("content", "")
                
                if "=" in content:
                    key, value = content.split("=", 1)
                    prefs[key] = self.get(key)
        
        return prefs
    
    def delete(self, key: str):
        """Delete preference"""
        for mem in self.memory.get_all():
            if key in mem.get("content", ""):
                self.memory.forget(mem["id"])


def demo():
    """Demo preferences"""
    memory = Memory(storage="json", path="./pref_demo.json")
    prefs = Preferences(memory, user_id="alice")
    
    print("=== Preferences Demo ===\n")
    
    # Set preferences
    prefs.set("theme", "dark")
    prefs.set("notifications", "true")
    prefs.set("volume", 80)
    
    print("Set preferences:")
    print(f"  theme: {prefs.get('theme')}")
    print(f"  notifications: {prefs.get('notifications')}")
    print(f"  volume: {prefs.get('volume')}")
    print(f"  unknown: {prefs.get('unknown', 'default_value')}")
    
    # Get all
    print(f"\nAll prefs: {prefs.get_all()}")
    
    # Cleanup
    import os
    if os.path.exists("./pref_demo.json"):
        os.remove("./pref_demo.json")


if __name__ == "__main__":
    demo()
