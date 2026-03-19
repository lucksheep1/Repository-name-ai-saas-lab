"""
Event-Driven Memory System
React to events and automatically update/retrieve memories
"""
from agent_memory import Memory
from typing import Callable, Dict, List
import re


class EventDrivenMemory:
    """Memory that reacts to events"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.triggers: Dict[str, List[Callable]] = {
            "on_add": [],
            "on_retrieve": [],
            "on_search": [],
            "on_update": [],
            "on_delete": [],
        }
    
    def register_trigger(self, event: str, callback: Callable):
        """Register a trigger for an event"""
        if event not in self.triggers:
            self.triggers[event] = []
        self.triggers[event].append(callback)
    
    def _fire(self, event: str, *args, **kwargs):
        """Fire all triggers for an event"""
        for callback in self.triggers.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print(f"Trigger error: {e}")
    
    def add_with_triggers(self, content: str, **kwargs):
        """Add memory and fire on_add triggers"""
        mem_id = self.memory.add(content, **kwargs)
        self._fire("on_add", mem_id, content, kwargs)
        return mem_id
    
    def search_with_triggers(self, query: str, **kwargs):
        """Search and fire on_search triggers"""
        results = self.memory.search(query, **kwargs)
        self._fire("on_search", query, results)
        return results
    
    def get_with_triggers(self, mem_id: str):
        """Get memory and fire on_retrieve triggers"""
        result = self.memory.get(mem_id)
        self._fire("on_retrieve", mem_id, result)
        return result


# Example triggers
def log_add_trigger(mem_id: str, content: str, kwargs: dict):
    """Log when memory is added"""
    print(f"📝 Added memory #{mem_id}: {content[:50]}...")


def analytics_trigger(mem_id: str, content: str, kwargs: dict):
    """Track analytics on add"""
    tags = kwargs.get("tags", [])
    priority = kwargs.get("priority", "none")
    print(f"   📊 Tags: {tags}, Priority: {priority}")


def keyword_alert_trigger(mem_id: str, content: str, kwargs: dict):
    """Alert on specific keywords"""
    alerts = ["error", "bug", "critical", "urgent"]
    content_lower = content.lower()
    
    for keyword in alerts:
        if keyword in content_lower:
            print(f"   🚨 ALERT: Found keyword '{keyword}' in memory!")
            break


def search_logger_trigger(query: str, results: list):
    """Log search queries"""
    print(f"🔍 Search: '{query}' → {len(results)} results")


class ConditionalMemory:
    """Memory with conditional logic"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.rules = []
    
    def add_rule(self, condition: Callable, action: Callable):
        """Add a conditional rule"""
        self.rules.append((condition, action))
    
    def add_with_rules(self, content: str, **kwargs):
        """Add memory and evaluate rules"""
        mem_id = self.memory.add(content, **kwargs)
        
        for condition, action in self.rules:
            if condition(content, kwargs):
                action(mem_id, content, kwargs)
        
        return mem_id


# Example rules
def auto_tag_rule(content: str, kwargs: dict) -> bool:
    """Auto-tag based on content"""
    content_lower = content.lower()
    
    new_tags = list(kwargs.get("tags", []))
    
    if "error" in content_lower or "bug" in content_lower:
        if "bug" not in new_tags:
            new_tags.append("bug")
    if "important" in content_lower or "urgent" in content_lower:
        if "important" not in new_tags:
            new_tags.append("important")
    
    if new_tags != kwargs.get("tags", []):
        kwargs["tags"] = new_tags
        return True
    
    return False


def auto_priority_rule(content: str, kwargs: dict) -> bool:
    """Auto-set priority based on keywords"""
    content_lower = content.lower()
    
    if "urgent" in content_lower or "critical" in content_lower:
        kwargs["priority"] = "high"
        return True
    elif "low" in content_lower or "minor" in content_lower:
        kwargs["priority"] = "low"
        return True
    
    return False


def demo():
    """Demo event-driven memory"""
    memory = Memory(storage="json", path="./event_demo.json")
    
    print("=== Event-Driven Memory Demo ===\n")
    
    # Setup event-driven memory
    edm = EventDrivenMemory(memory)
    edm.register_trigger("on_add", log_add_trigger)
    edm.register_trigger("on_add", analytics_trigger)
    edm.register_trigger("on_add", keyword_alert_trigger)
    edm.register_trigger("on_search", search_logger_trigger)
    
    # Add memories (triggers will fire)
    print("Adding memories:\n")
    edm.add_with_triggers("User logged in successfully", tags=["auth"])
    edm.add_with_triggers("Critical error in payment system", tags=["error"], priority="high")
    edm.add_with_triggers("User submitted bug report #123", tags=["bug"])
    
    print("\nSearching:\n")
    edm.search_with_triggers("error")
    
    # Conditional memory demo
    print("\n=== Conditional Memory Demo ===\n")
    
    cm = ConditionalMemory(memory)
    cm.add_rule(auto_tag_rule, lambda *a: None)
    cm.add_rule(auto_priority_rule, lambda *a: None)
    
    cm.add_with_rules("This is an urgent matter", tags=["task"])
    cm.add_with_rules("Minor bug found in UI", tags=["task"])
    
    # Cleanup
    import os
    if os.path.exists("./event_demo.json"):
        os.remove("./event_demo.json")


if __name__ == "__main__":
    demo()
