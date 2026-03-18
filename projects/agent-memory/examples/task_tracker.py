#!/usr/bin/env python3
"""
Agent Memory - Task Tracker
==========================
Track tasks with memory.

Usage:
    from task_tracker import TaskTracker
    
    tracker = TaskTracker()
    tracker.add_task("Fix bug")
    tracker.complete_task("Fix bug")
    tracker.get_pending()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Optional
from agent_memory import Memory


class TaskTracker:
    """Task tracking with memory."""
    
    def __init__(self, storage: str = "json", path: str = "./memory.json"):
        self.memory = Memory(storage=storage, path=path)
    
    def add_task(self, task: str, tags: List[str] = None, priority: int = 3) -> str:
        """Add a task."""
        tags = tags or ["task", "pending"]
        metadata = {"status": "pending", "priority": priority, "type": "task"}
        
        return self.memory.add_with_tags(task, tags=tags, metadata=metadata)
    
    def complete_task(self, task_id: str) -> bool:
        """Mark task as completed."""
        # Get the task
        recent = self.memory.get_recent(limit=self.memory.count())
        
        for mem in recent:
            if mem["id"] == task_id:
                text = mem["text"]
                old_tags = mem.get("tags", [])
                old_metadata = mem.get("metadata", {})
                
                # Update tags and metadata
                new_tags = [t for t in old_tags if t != "pending"]
                new_tags.append("completed")
                
                # Delete and re-add
                self.memory.delete(task_id)
                self.memory.add_with_tags(
                    text, 
                    tags=new_tags,
                    metadata={**old_metadata, "status": "completed"}
                )
                return True
        
        return False
    
    def get_pending(self, limit: int = 20) -> List[Dict]:
        """Get pending tasks."""
        return self.memory.get_by_tag("pending")
    
    def get_completed(self, limit: int = 20) -> List[Dict]:
        """Get completed tasks."""
        return self.memory.get_by_tag("completed")
    
    def get_all_tasks(self, limit: int = 50) -> List[Dict]:
        """Get all tasks."""
        return self.memory.get_recent(limit=limit)
    
    def get_stats(self) -> Dict:
        """Get task statistics."""
        pending = self.get_pending()
        completed = self.get_completed()
        
        return {
            "total": len(pending) + len(completed),
            "pending": len(pending),
            "completed": len(completed)
        }


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "task_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Task Tracker Demo")
    print("=" * 50)
    
    tracker = TaskTracker(storage="json", path=demo_path)
    
    # Add tasks
    print("\n1. Adding tasks...")
    t1 = tracker.add_task("Fix login bug", priority=5)
    t2 = tracker.add_task("Add dark mode", priority=3)
    t3 = tracker.add_task("Write tests", priority=2)
    t4 = tracker.add_task("Update docs", priority=1)
    
    print(f"   Added 4 tasks")
    
    # Get pending
    print("\n2. Pending tasks:")
    pending = tracker.get_pending()
    for p in pending:
        pr = p.get("metadata", {}).get("priority", 0)
        print(f"   [P{pr}] {p['text']}")
    
    # Complete a task
    print("\n3. Completing task:", t1)
    tracker.complete_task(t1)
    
    # Show stats
    print("\n4. Stats:")
    stats = tracker.get_stats()
    print(f"   Total: {stats['total']}")
    print(f"   Pending: {stats['pending']}")
    print(f"   Completed: {stats['completed']}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
