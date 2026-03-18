#!/usr/bin/env python3
"""
Agent Memory - Notification System
=================================
Get notified when important memories are added.

Usage:
    from notifications import MemoryNotifier
    
    notifier = MemoryNotifier(memory)
    notifier.watch("urgent", send_alert)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Callable, List, Dict
from agent_memory import Memory


class MemoryNotifier:
    """Notification system for memory events."""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.watchers: Dict[str, List[Callable]] = {}
    
    def watch(self, tag: str, callback: Callable):
        """Watch for memories with specific tag."""
        if tag not in self.watchers:
            self.watchers[tag] = []
        self.watchers[tag].append(callback)
    
    def unwatch(self, tag: str, callback: Callable = None):
        """Stop watching a tag."""
        if tag in self.watchers:
            if callback:
                self.watchers[tag].remove(callback)
            else:
                del self.watchers[tag]
    
    def notify(self, memory_id: str, text: str, tags: List[str], metadata: dict):
        """Notify watchers of new memory."""
        for tag in tags:
            if tag in self.watchers:
                for callback in self.watchers[tag]:
                    try:
                        callback({
                            "id": memory_id,
                            "text": text,
                            "tags": tags,
                            "metadata": metadata
                        })
                    except Exception as e:
                        print(f"Notification error: {e}")
    
    def add(self, text: str, metadata: dict = None, ttl_days: int = None) -> str:
        """Add memory and notify watchers."""
        # Get tags before adding
        tags = metadata.get("tags", []) if metadata else []
        
        # Add memory
        memory_id = self.memory.add(text, metadata, ttl_days)
        
        # Get the added memory with tags
        recent = self.memory.get_recent(limit=1)
        if recent and recent[0]["id"] == memory_id:
            actual_tags = recent[0].get("tags", [])
            self.notify(memory_id, text, actual_tags, metadata or {})
        
        return memory_id
    
    def add_with_tags(self, text: str, tags: List[str], metadata: dict = None) -> str:
        """Add memory with tags and notify."""
        memory_id = self.memory.add_with_tags(text, tags, metadata)
        self.notify(memory_id, text, tags, metadata or {})
        return memory_id


# Demo callbacks
def print_alert(memory):
    """Print alert for urgent memories."""
    print(f"   🚨 URGENT: {memory['text']}")


def print_bug(memory):
    """Print alert for bug memories."""
    print(f"   🐛 BUG: {memory['text']}")


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "notification_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Notification Demo")
    print("=" * 50)
    
    memory = Memory(storage="json", path=demo_path)
    notifier = MemoryNotifier(memory)
    
    # Set up watchers
    print("\n1. Setting up watchers...")
    notifier.watch("urgent", print_alert)
    notifier.watch("bug", print_bug)
    print("   Watching: urgent, bug")
    
    # Add memories
    print("\n2. Adding memories...")
    notifier.add("Normal task", metadata={"tags": ["task"]})
    print("   Added: Normal task")
    
    notifier.add_with_tags("Fix critical bug!", tags=["bug", "urgent"])
    print("   Added: Fix critical bug!")
    
    notifier.add_with_tags("Server is down!", tags=["urgent"])
    print("   Added: Server is down!")
    
    notifier.add("Regular reminder", metadata={"tags": ["reminder"]})
    print("   Added: Regular reminder")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
