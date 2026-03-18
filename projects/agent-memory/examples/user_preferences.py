#!/usr/bin/env python3
"""
Agent Memory - User Preferences
==============================
Store and retrieve user preferences.

Usage:
    from user_preferences import UserPreferences
    
    prefs = UserPreferences()
    prefs.set("theme", "dark")
    prefs.set("language", "en")
    theme = prefs.get("theme")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Dict, Optional
from agent_memory import Memory


class UserPreferences:
    """User preferences stored in memory."""
    
    def __init__(self, user_id: str = "default", storage: str = "json", path: str = "./memory.json"):
        self.user_id = user_id
        self.memory = Memory(storage=storage, path=path)
        self.prefix = f"pref:{user_id}:"
    
    def set(self, key: str, value: Any):
        """Set a preference."""
        text = f"{self.prefix}{key}: {value}"
        tags = ["preference", self.user_id]
        metadata = {"key": key, "value": value, "type": "preference", "user_id": self.user_id}
        
        # Delete old preference first
        self._delete(key)
        
        # Add new
        self.memory.add_with_tags(text, tags=tags, metadata=metadata)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a preference."""
        recent = self.memory.get_recent(limit=self.memory.count())
        
        for mem in recent:
            if mem.get("metadata", {}).get("key") == key:
                if mem.get("metadata", {}).get("user_id") == self.user_id:
                    return mem.get("metadata", {}).get("value", default)
        
        return default
    
    def _delete(self, key: str):
        """Delete a preference."""
        recent = self.memory.get_recent(limit=self.memory.count())
        
        for mem in recent:
            if mem.get("metadata", {}).get("key") == key:
                if mem.get("metadata", {}).get("user_id") == self.user_id:
                    self.memory.delete(mem["id"])
    
    def delete(self, key: str):
        """Delete a preference."""
        self._delete(key)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all preferences."""
        recent = self.memory.get_recent(limit=self.memory.count())
        
        prefs = {}
        for mem in recent:
            md = mem.get("metadata", {})
            if md.get("type") == "preference" and md.get("user_id") == self.user_id:
                key = md.get("key")
                value = md.get("value")
                if key:
                    prefs[key] = value
        
        return prefs
    
    def clear(self):
        """Clear all preferences for user."""
        recent = self.memory.get_recent(limit=self.memory.count())
        
        for mem in recent:
            if mem.get("metadata", {}).get("user_id") == self.user_id:
                if "preference" in mem.get("tags", []):
                    self.memory.delete(mem["id"])


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "prefs_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - User Preferences Demo")
    print("=" * 50)
    
    prefs = UserPreferences(storage="json", path=demo_path)
    
    # Set preferences
    print("\n1. Setting preferences...")
    prefs.set("theme", "dark")
    prefs.set("language", "en")
    prefs.set("notifications", True)
    prefs.set("font_size", 14)
    
    print("   Set: theme=dark, language=en, notifications=True, font_size=14")
    
    # Get preferences
    print("\n2. Getting preferences...")
    print(f"   theme: {prefs.get('theme')}")
    print(f"   language: {prefs.get('language')}")
    print(f"   notifications: {prefs.get('notifications')}")
    print(f"   font_size: {prefs.get('font_size')}")
    
    # Get all
    print("\n3. All preferences:")
    all_prefs = prefs.get_all()
    for key, value in all_prefs.items():
        print(f"   {key}: {value}")
    
    # Delete one
    print("\n4. Deleting font_size...")
    prefs.delete("font_size")
    print(f"   font_size: {prefs.get('font_size', 'not found')}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
