#!/usr/bin/env python3
"""
Agent Memory - Event-Driven Updates
===================================
Use agent-memory with event-driven architecture.

This example shows how to:
- Store memory events
- React to memory changes
- Build event handlers

Usage:
    python event_driver.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory
from typing import Callable, List, Dict, Any


class MemoryEvent:
    """Memory event."""
    def __init__(self, event_type: str, data: dict):
        self.type = event_type
        self.data = data
        self.timestamp = None


class EventDrivenMemory(Memory):
    """Memory with event system."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handlers: Dict[str, List[Callable]] = {
            "add": [],
            "search": [],
            "delete": [],
            "clear": []
        }
    
    def on(self, event_type: str, handler: Callable):
        """Register event handler."""
        if event_type in self.handlers:
            self.handlers[event_type].append(handler)
    
    def _emit(self, event_type: str, data: dict):
        """Emit event to handlers."""
        event = MemoryEvent(event_type, data)
        for handler in self.handlers.get(event_type, []):
            try:
                handler(event)
            except Exception as e:
                print(f"Handler error: {e}")
    
    def add(self, text: str, metadata: dict = None, ttl_days: int = None) -> str:
        """Add memory and emit event."""
        result = super().add(text, metadata, ttl_days)
        self._emit("add", {"id": result, "text": text, "metadata": metadata})
        return result
    
    def search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search and emit event."""
        results = super().search(query, top_k)
        self._emit("search", {"query": query, "count": len(results)})
        return results
    
    def delete(self, memory_id: str) -> bool:
        """Delete and emit event."""
        result = super().delete(memory_id)
        if result:
            self._emit("delete", {"id": memory_id})
        return result
    
    def clear(self):
        """Clear and emit event."""
        count = self.count()
        super().clear()
        self._emit("clear", {"count": count})


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "event_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Event-Driven Demo")
    print("=" * 50)
    
    # Create event-driven memory
    memory = EventDrivenMemory(storage="json", path=demo_path)
    
    # Register handlers
    def on_add(event):
        print(f"📝 ADDED: {event.data['text'][:40]}")
    
    def on_search(event):
        print(f"🔍 SEARCH: '{event.data['query']}' found {event.data['count']} results")
    
    def on_delete(event):
        print(f"🗑️ DELETED: {event.data['id']}")
    
    def on_clear(event):
        print(f"🧹 CLEARED: {event.data['count']} memories")
    
    memory.on("add", on_add)
    memory.on("search", on_search)
    memory.on("delete", on_delete)
    memory.on("clear", on_clear)
    
    # Use memory
    print("\n1. Adding memories:")
    memory.add("Remember to buy milk")
    memory.add("Call mom tomorrow")
    memory.add("Finish the project")
    
    print("\n2. Searching:")
    memory.search("milk")
    memory.search("project")
    
    print("\n3. Getting context:")
    context = memory.get_context()
    print(context[:200])
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
