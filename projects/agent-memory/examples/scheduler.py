#!/usr/bin/env python3
"""
Agent Memory - Scheduled Cleanup
================================
Automatically clean up old memories.

Usage:
    from scheduler import ScheduledCleanup
    
    cleanup = ScheduledCleanup(memory)
    cleanup.run_daily()  # Run daily cleanup
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from datetime import datetime, timedelta
from typing import List, Dict
from agent_memory import Memory


class ScheduledCleanup:
    """Scheduled cleanup for memory."""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_old_memories(self, days: int = 30) -> List[dict]:
        """Get memories older than specified days."""
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()
        
        all_memories = self.memory.get_recent(limit=self.memory.count())
        old = [m for m in all_memories if m.get("timestamp", "") < cutoff_str]
        
        return old
    
    def cleanup_old(self, days: int = 30, min_priority: int = 3) -> int:
        """Clean up old memories with low priority."""
        old = self.get_old_memories(days)
        
        deleted = 0
        for mem in old:
            priority = mem.get("priority", 0)
            if priority < min_priority:
                if self.memory.delete(mem["id"]):
                    deleted += 1
        
        return deleted
    
    def cleanup_by_tag(self, tag: str) -> int:
        """Clean up memories with specific tag."""
        tagged = self.memory.get_by_tag(tag)
        
        deleted = 0
        for mem in tagged:
            if self.memory.delete(mem["id"]):
                deleted += 1
        
        return deleted
    
    def get_stats(self) -> dict:
        """Get cleanup statistics."""
        total = self.memory.count()
        
        # Count by age
        now = datetime.now()
        ages = {"week": 0, "month": 0, "older": 0}
        
        recent = self.memory.get_recent(limit=total)
        for mem in recent:
            ts = mem.get("timestamp", "")
            if ts:
                try:
                    mem_time = datetime.fromisoformat(ts[:19])
                    age = (now - mem_time).days
                    
                    if age < 7:
                        ages["week"] += 1
                    elif age < 30:
                        ages["month"] += 1
                    else:
                        ages["older"] += 1
                except:
                    pass
        
        return {
            "total": total,
            "age_distribution": ages,
            "can_cleanup": ages["older"]
        }


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "cleanup_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Scheduled Cleanup Demo")
    print("=" * 50)
    
    memory = Memory(storage="json", path=demo_path)
    
    # Add some memories
    print("\n1. Adding memories...")
    memory.add("Task A", metadata={"priority": 1})
    memory.add("Task B", metadata={"priority": 2})
    memory.add("Task C", metadata={"priority": 3})
    memory.add("Task D", metadata={"priority": 4})
    memory.add("Task E", metadata={"priority": 5})
    
    print(f"   Total: {memory.count()}")
    
    # Cleanup
    cleanup = ScheduledCleanup(memory)
    
    print("\n2. Cleanup stats:")
    stats = cleanup.get_stats()
    print(f"   Total: {stats['total']}")
    print(f"   Age distribution: {stats['age_distribution']}")
    print(f"   Can cleanup (older): {stats['can_cleanup']}")
    
    print("\n3. Cleanup low priority (P<3):")
    deleted = cleanup.cleanup_old(days=0, min_priority=3)
    print(f"   Deleted: {deleted}")
    print(f"   Remaining: {memory.count()}")
    
    # Show remaining
    print("\n4. Remaining memories:")
    recent = memory.get_recent(limit=10)
    for mem in recent:
        p = mem.get("priority", 0)
        print(f"   [P{p}] {mem['text']}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
