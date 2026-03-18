#!/usr/bin/env python3
"""
Agent Memory - Multi-User Support
================================
Share memory across multiple users with access control.

Usage:
    from multiuser import MultiUserMemory
    
    memory = MultiUserMemory()
    memory.add("Secret", owner="user1", allowed=["user1", "user2"])
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional
from agent_memory import Memory


class MultiUserMemory(Memory):
    """Memory with multi-user support."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def add(self, text: str, metadata: dict = None, ttl_days: int = None,
            owner: str = None, allowed: List[str] = None) -> str:
        """Add memory with ownership."""
        metadata = metadata or {}
        
        if owner:
            metadata["owner"] = owner
        if allowed:
            metadata["allowed"] = allowed
        
        return super().add(text, metadata, ttl_days)
    
    def get_by_owner(self, owner: str, limit: int = 10) -> List[dict]:
        """Get memories by owner."""
        all_memories = self.get_recent(limit=self.count())
        owned = [m for m in all_memories 
                if m.get("metadata", {}).get("owner") == owner]
        return owned[:limit]
    
    def get_shared_with(self, user: str, limit: int = 10) -> List[dict]:
        """Get memories shared with user."""
        all_memories = self.get_recent(limit=self.count())
        shared = []
        
        for m in all_memories:
            allowed = m.get("metadata", {}).get("allowed", [])
            if user in allowed:
                shared.append(m)
        
        return shared[:limit]
    
    def can_access(self, memory_id: str, user: str) -> bool:
        """Check if user can access memory."""
        recent = self.get_recent(limit=self.count())
        
        for mem in recent:
            if mem["id"] == memory_id:
                metadata = mem.get("metadata", {})
                
                # Owner can always access
                if metadata.get("owner") == user:
                    return True
                
                # Check allowed list
                allowed = metadata.get("allowed", [])
                if user in allowed:
                    return True
                
                # No restrictions
                if not metadata.get("owner") and not allowed:
                    return True
                
                return False
        
        return False


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "multiuser_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Multi-User Demo")
    print("=" * 50)
    
    memory = MultiUserMemory(storage="json", path=demo_path)
    
    # Add memories with owners
    print("\n1. Adding memories...")
    memory.add("User1's private note", owner="user1")
    memory.add("User2's private note", owner="user2")
    memory.add("Shared between user1 and user2", owner="user1", allowed=["user1", "user2"])
    memory.add("Team task", owner="admin", allowed=["user1", "user2", "admin"])
    
    print(f"   Total: {memory.count()}")
    
    # Get by owner
    print("\n2. User1's memories:")
    user1_memories = memory.get_by_owner("user1")
    for mem in user1_memories:
        print(f"   - {mem['text']}")
    
    print("\n3. User2's memories:")
    user2_memories = memory.get_by_owner("user2")
    for mem in user2_memories:
        print(f"   - {mem['text']}")
    
    # Get shared
    print("\n4. Memories shared with user1:")
    shared = memory.get_shared_with("user1")
    for mem in shared:
        print(f"   - {mem['text']}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
