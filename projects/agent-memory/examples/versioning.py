#!/usr/bin/env python3
"""
Agent Memory - Version Control
===============================
Version control for memories.

Usage:
    from versioning import VersionedMemory
    
    memory = VersionedMemory()
    memory.add("Original text")
    memory.update("memory_id", "Updated text")
    history = memory.get_history("memory_id")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from typing import List, Dict, Optional
from agent_memory import Memory


class VersionedMemory(Memory):
    """Memory with version control."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.versions: Dict[str, List[dict]] = {}
    
    def add(self, text: str, metadata: dict = None, ttl_days: int = None) -> str:
        """Add memory and create initial version."""
        memory_id = super().add(text, metadata, ttl_days)
        
        # Create initial version
        self.versions[memory_id] = [{
            "version": 1,
            "text": text,
            "timestamp": time.time(),
            "metadata": metadata
        }]
        
        return memory_id
    
    def update(self, memory_id: str, new_text: str) -> bool:
        """Update memory and create new version."""
        # Get current memory
        recent = self.get_recent(limit=self.count())
        found = None
        for mem in recent:
            if mem["id"] == memory_id:
                found = mem
                break
        
        if not found:
            return False
        
        # Delete old
        self.delete(memory_id)
        
        # Add new
        metadata = found.get("metadata", {})
        new_id = self.add(new_text, metadata)
        
        # Copy version history
        if memory_id in self.versions:
            old_versions = self.versions[memory_id].copy()
            new_version = {
                "version": len(old_versions) + 1,
                "text": new_text,
                "timestamp": time.time(),
                "metadata": metadata
            }
            old_versions.append(new_version)
            self.versions[new_id] = old_versions
        
        return True
    
    def get_history(self, memory_id: str) -> List[dict]:
        """Get version history of a memory."""
        return self.versions.get(memory_id, [])
    
    def revert_to(self, memory_id: str, version: int) -> bool:
        """Revert memory to a specific version."""
        history = self.get_history(memory_id)
        
        target = None
        for v in history:
            if v["version"] == version:
                target = v
                break
        
        if not target:
            return False
        
        return self.update(memory_id, target["text"])


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "version_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Version Control Demo")
    print("=" * 50)
    
    memory = VersionedMemory(storage="json", path=demo_path)
    
    # Add memory
    print("\n1. Adding memory...")
    memory_id = memory.add("Original task description")
    print(f"   ID: {memory_id}")
    print(f"   Text: Original task description")
    
    # Update
    print("\n2. Updating memory...")
    memory.update(memory_id, "Updated task description - added priority")
    print(f"   Text: Updated task description - added priority")
    
    # Update again
    print("\n3. Updating again...")
    memory.update(memory_id, "Final task description - complete")
    print(f"   Text: Final task description - complete")
    
    # Show history
    print("\n4. Version history:")
    history = memory.get_history(memory_id)
    for v in history:
        print(f"   v{v['version']}: {v['text']}")
    
    # Revert
    print("\n5. Reverting to v1...")
    memory.revert_to(memory_id, 1)
    recent = memory.get_recent(limit=1)
    if recent and recent[0]["id"] == memory_id:
        print(f"   Current: {recent[0]['text']}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
