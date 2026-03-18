#!/usr/bin/env python3
"""
Agent Memory - Automation Triggers
==================================
Trigger actions based on memory events.

Usage:
    from triggers import TriggerMemory
    
    memory = TriggerMemory()
    memory.when("tag:urgent").send_webhook("https://hooks.example.com/alert")
    memory.when("tag:bug").create_issue("https://github.com/...")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from typing import Callable, Dict, List
from agent_memory import Memory


class Trigger:
    """Trigger condition."""
    def __init__(self, condition: str, action: Callable):
        self.condition = condition
        self.action = action
    
    def match(self, text: str, tags: List[str]) -> bool:
        """Check if trigger matches."""
        if self.condition.startswith("tag:"):
            required_tag = self.condition[4:]
            return required_tag in tags
        elif self.condition.startswith("text:"):
            required_text = self.condition[5:]
            return required_text.lower() in text.lower()
        return False


class TriggerMemory(Memory):
    """Memory with automation triggers."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggers: List[Trigger] = []
    
    def when(self, condition: str) -> 'TriggerBuilder':
        """Create a trigger builder."""
        return TriggerBuilder(self, condition)
    
    def add_trigger(self, condition: str, action: Callable):
        """Add a trigger."""
        trigger = Trigger(condition, action)
        self.triggers.append(trigger)
    
    def _fire_triggers(self, text: str, tags: List[str], metadata: dict):
        """Fire matching triggers."""
        for trigger in self.triggers:
            if trigger.match(text, tags):
                try:
                    trigger.action({
                        "text": text,
                        "tags": tags,
                        "metadata": metadata,
                        "timestamp": time.time()
                    })
                except Exception as e:
                    print(f"Trigger error: {e}")
    
    def add_with_tags(self, text: str, tags: List[str], metadata: dict = None) -> str:
        """Add memory and fire triggers."""
        memory_id = super().add_with_tags(text, tags, metadata)
        self._fire_triggers(text, tags, metadata or {})
        return memory_id
    
    def add(self, text: str, metadata: dict = None, ttl_days: int = None) -> str:
        """Add memory and fire triggers."""
        memory_id = super().add(text, metadata, ttl_days)
        
        # Get tags from added memory
        recent = self.get_recent(limit=1)
        if recent:
            tags = recent[0].get("tags", [])
            self._fire_triggers(text, tags, metadata or {})
        
        return memory_id


class TriggerBuilder:
    """Builder for triggers."""
    def __init__(self, memory: TriggerMemory, condition: str):
        self.memory = memory
        self.condition = condition
    
    def do(self, action: Callable):
        """Register action."""
        self.memory.add_trigger(self.condition, action)
        return self.memory


# Demo actions
def webhook_alert(data):
    """Webhook alert action."""
    print(f"   📡 WEBHOOK: {data['text'][:30]}...")


def log_to_console(data):
    """Log to console action."""
    print(f"   📝 LOG: {data['text']}")


def create_issue(data):
    """Create issue action."""
    print(f"   🔧 ISSUE: Would create issue for '{data['text'][:30]}'")


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "trigger_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Triggers Demo")
    print("=" * 50)
    
    memory = TriggerMemory(storage="json", path=demo_path)
    
    # Set up triggers
    print("\n1. Setting up triggers...")
    memory.when("tag:urgent").do(webhook_alert)
    memory.when("tag:bug").do(create_issue)
    memory.when("text:important").do(log_to_console)
    print("   - tag:urgent -> webhook")
    print("   - tag:bug -> create issue")
    print("   - text:important -> log")
    
    # Add memories (triggers will fire)
    print("\n2. Adding memories...")
    
    print("   Adding: Fix urgent bug!")
    memory.add_with_tags("Fix urgent bug!", tags=["bug", "urgent"])
    
    print("   Adding: Regular task")
    memory.add("Regular task")
    
    print("   Adding: Important information")
    memory.add("Important information")
    
    print("   Adding: Another urgent thing")
    memory.add_with_tags("Another urgent thing", tags=["urgent"])
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
