#!/usr/bin/env python3
"""
Agent Memory - Priority Queue
=============================
Use memory with priority queue semantics.

Usage:
    from priority_queue import PriorityMemory
    
    memory = PriorityMemory()
    memory.add("Critical task", priority=5)
    memory.add("Low priority", priority=1)
    
    # Get highest priority first
    important = memory.get_by_priority(4)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any
from agent_memory import Memory


class PriorityMemory(Memory):
    """Memory with priority queue features."""
    
    def get_priority_queue(self, min_priority: int = 1) -> List[dict]:
        """Get memories sorted by priority (highest first)."""
        all_memories = self.get_recent(limit=self.count())
        
        # Filter by priority
        filtered = [m for m in all_memories if m.get("priority", 0) >= min_priority]
        
        # Sort by priority (descending)
        filtered.sort(key=lambda x: x.get("priority", 0), reverse=True)
        
        return filtered
    
    def get_next_task(self) -> dict:
        """Get the highest priority memory as next task."""
        queue = self.get_priority_queue(min_priority=1)
        return queue[0] if queue else None
    
    def complete_task(self, memory_id: str) -> bool:
        """Mark a task as complete and remove it."""
        return self.delete(memory_id)
    
    def reschedule(self, memory_id: str, new_priority: int) -> bool:
        """Change priority of a memory."""
        # Get the memory
        recent = self.get_recent(limit=self.count())
        for mem in recent:
            if mem["id"] == memory_id:
                # Update - delete and re-add with new priority
                text = mem["text"]
                metadata = mem.get("metadata", {})
                metadata["priority"] = new_priority
                
                self.delete(memory_id)
                self.add(text, metadata=metadata)
                return True
        return False


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "priority_queue_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Priority Queue Demo")
    print("=" * 50)
    
    # Create priority memory
    memory = PriorityMemory(storage="json", path=demo_path)
    
    # Add tasks with priorities
    print("\n1. Adding tasks with priorities...")
    memory.add("Fix critical bug in production", metadata={"priority": 5})
    memory.add("Write unit tests", metadata={"priority": 2})
    memory.add("Update documentation", metadata={"priority": 1})
    memory.add("Review pull requests", metadata={"priority": 3})
    memory.add("Deploy to staging", metadata={"priority": 4})
    
    # Get priority queue
    print("\n2. Priority queue (all tasks):")
    queue = memory.get_priority_queue()
    for i, task in enumerate(queue, 1):
        p = task.get("priority", 0)
        print(f"   {i}. [P{p}] {task['text']}")
    
    # Get next task
    print("\n3. Next task to do:")
    next_task = memory.get_next_task()
    print(f"   [P{next_task.get('priority', 0)}] {next_task['text']}")
    
    # Get high priority only
    print("\n4. High priority tasks (P4+):")
    high = memory.get_priority_queue(min_priority=4)
    for task in high:
        print(f"   [P{task.get('priority', 0)}] {task['text']}")
    
    # Complete the top task
    print("\n5. Completing top task...")
    memory.complete_task(next_task["id"])
    print("   Done!")
    
    # Show remaining
    print("\n6. Remaining tasks:")
    queue = memory.get_priority_queue()
    for i, task in enumerate(queue, 1):
        p = task.get("priority", 0)
        print(f"   {i}. [P{p}] {task['text']}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
