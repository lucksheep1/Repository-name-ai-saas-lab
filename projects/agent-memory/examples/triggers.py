"""
Memory Triggers
Event-driven memory triggers
"""
from agent_memory import Memory
from typing import Callable, Dict, List


class Trigger:
    """Memory trigger"""
    
    def __init__(self, name: str, condition: Callable, action: Callable):
        self.name = name
        self.condition = condition
        self.action = action
    
    def evaluate(self, mem: dict) -> bool:
        """Evaluate trigger condition"""
        try:
            return self.condition(mem)
        except:
            return False
    
    def execute(self, mem: dict):
        """Execute trigger action"""
        try:
            self.action(mem)
        except Exception as e:
            print(f"Trigger error: {e}")


class TriggerManager:
    """Manage memory triggers"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.triggers: List[Trigger] = []
    
    def register(self, trigger: Trigger):
        """Register trigger"""
        self.triggers.append(trigger)
    
    def check(self, mem: dict):
        """Check all triggers for memory"""
        for trigger in self.triggers:
            if trigger.evaluate(mem):
                trigger.execute(mem)


# Pre-built triggers
def urgent_trigger(mem: dict) -> bool:
    """Trigger on urgent memories"""
    tags = mem.get("tags", [])
    return "urgent" in tags or mem.get("metadata", {}).get("priority", 0) >= 4


def log_trigger(mem: dict):
    """Log trigger action"""
    print(f"📢 URGENT: {mem.get('content', '')[:50]}")


def tag_trigger(tag: str) -> Trigger:
    """Create tag-based trigger"""
    def condition(m: dict) -> bool:
        return tag in m.get("tags", [])
    
    def action(m: dict):
        print(f"🏷️ Tagged '{tag}': {m.get('content', '')[:50]}")
    
    return Trigger(f"tag_{tag}", condition, action)


def priority_trigger(min_priority: int) -> Trigger:
    """Create priority-based trigger"""
    def condition(m: dict) -> bool:
        return m.get("metadata", {}).get("priority", 0) >= min_priority
    
    def action(m: dict):
        print(f"⭐ High priority: {m.get('content', '')[:50]}")
    
    return Trigger(f"priority_{min_priority}", condition, action)


def keyword_trigger(keyword: str) -> Trigger:
    """Create keyword-based trigger"""
    keyword_lower = keyword.lower()
    
    def condition(m: dict) -> bool:
        return keyword_lower in m.get("content", "").lower()
    
    def action(m: dict):
        print(f"🔑 Keyword '{keyword}': {m.get('content', '')[:50]}")
    
    return Trigger(f"keyword_{keyword}", condition, action)


def demo():
    """Demo triggers"""
    memory = Memory(storage="json", path="./trigger_demo.json")
    manager = TriggerManager(memory)
    
    print("=== Memory Triggers Demo ===\n")
    
    # Register triggers
    manager.register(tag_trigger("bug"))
    manager.register(priority_trigger(4))
    manager.register(keyword_trigger("error"))
    
    # Add memories (triggers will fire)
    memory.add("Normal conversation")
    memory.add("Important meeting", priority=4)
    memory.add("Bug in code", tags=["bug"])
    memory.add("Error occurred", tags=["error"])
    
    print("\nAll memories:")
    for m in memory.get_all():
        print(f"  {m.get('content')[:40]}")
    
    # Cleanup
    import os
    if os.path.exists("./trigger_demo.json"):
        os.remove("./trigger_demo.json")


if __name__ == "__main__":
    demo()
