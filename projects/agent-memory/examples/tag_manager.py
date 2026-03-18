#!/usr/bin/env python3
"""
Agent Memory - Memory Tags Manager
==================================
Advanced tag management.

Usage:
    from tag_manager import TagManager
    
    manager = TagManager(memory)
    suggestions = manager.suggest_tags("New feature request")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Set
from collections import Counter
from agent_memory import Memory


class TagManager:
    """Advanced tag management."""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags."""
        all_memories = self.memory.get_recent(limit=self.memory.count())
        
        tags: Set[str] = set()
        for mem in all_memories:
            tags.update(mem.get("tags", []))
        
        return sorted(list(tags))
    
    def get_tag_counts(self) -> Dict[str, int]:
        """Get tag usage counts."""
        all_memories = self.memory.get_recent(limit=self.memory.count())
        
        tags = []
        for mem in all_memories:
            tags.extend(mem.get("tags", []))
        
        return dict(Counter(tags).most_common())
    
    def suggest_tags(self, text: str) -> List[str]:
        """Suggest tags based on text."""
        text_lower = text.lower()
        suggestions = []
        
        # Common tag patterns
        patterns = {
            "bug": ["bug", "error", "fix", "issue", "problem"],
            "feature": ["feature", "add", "new", "implement"],
            "urgent": ["urgent", "critical", "asap", "important"],
            "task": ["task", "todo", "do"],
            "meeting": ["meeting", "call", "sync"],
            "idea": ["idea", "thought", "consider"],
            "question": ["question", "help", "how", "what"],
        }
        
        for tag, keywords in patterns.items():
            if any(kw in text_lower for kw in keywords):
                suggestions.append(tag)
        
        return suggestions
    
    def merge_tags(self, source_tag: str, target_tag: str) -> int:
        """Merge source tag into target tag."""
        tagged = self.memory.get_by_tag(source_tag)
        
        merged = 0
        for mem in tagged:
            text = mem["text"]
            old_tags = mem.get("tags", [])
            
            if source_tag in old_tags:
                old_tags.remove(source_tag)
                if target_tag not in old_tags:
                    old_tags.append(target_tag)
                
                # Delete and re-add with new tags
                self.memory.delete(mem["id"])
                self.memory.add_with_tags(text, tags=old_tags, metadata=mem.get("metadata"))
                merged += 1
        
        return merged
    
    def split_tag(self, tag: str, new_tags: List[str]) -> int:
        """Split a tag into multiple tags."""
        tagged = self.memory.get_by_tag(tag)
        
        split = 0
        for mem in tagged:
            text = mem["text"]
            old_tags = mem.get("tags", [])
            
            # Remove old tag and add new ones
            if tag in old_tags:
                old_tags.remove(tag)
                for new_tag in new_tags:
                    if new_tag not in old_tags:
                        old_tags.append(new_tag)
                
                self.memory.delete(mem["id"])
                self.memory.add_with_tags(text, tags=old_tags, metadata=mem.get("metadata"))
                split += 1
        
        return split


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "tag_manager_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Tag Manager Demo")
    print("=" * 50)
    
    memory = Memory(storage="json", path=demo_path)
    manager = TagManager(memory)
    
    # Add memories with tags
    print("\n1. Adding memories...")
    memory.add_with_tags("Fix login bug", tags=["bug", "urgent"])
    memory.add_with_tags("Add dark mode", tags=["feature", "ui"])
    memory.add_with_tags("Fix memory leak", tags=["bug", "performance"])
    memory.add_with_tags("Add export feature", tags=["feature"])
    memory.add_with_tags("Urgent meeting", tags=["meeting", "urgent"])
    
    print(f"   Total: {memory.count()}")
    
    # Get all tags
    print("\n2. All tags:")
    all_tags = manager.get_all_tags()
    print(f"   {all_tags}")
    
    # Get tag counts
    print("\n3. Tag counts:")
    counts = manager.get_tag_counts()
    for tag, count in counts.items():
        print(f"   {tag}: {count}")
    
    # Suggest tags
    print("\n4. Tag suggestions:")
    suggestions = manager.suggest_tags("Add new feature to the UI")
    print(f"   'Add new feature to the UI' -> {suggestions}")
    
    suggestions = manager.suggest_tags("Critical bug in production")
    print(f"   'Critical bug in production' -> {suggestions}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
