"""
Memory Task Tracker
Track tasks and todos with memory
"""
from agent_memory import Memory
from datetime import datetime


class TaskTracker:
    """Track tasks using memory"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def add_task(self, title: str, due: str = None, priority: int = 3) -> str:
        """Add a task"""
        metadata = {
            "_task": True,
            "priority": priority,
            "status": "pending"
        }
        
        if due:
            metadata["due"] = due
        
        return self.memory.add(title, tags=["task"], metadata=metadata)
    
    def complete_task(self, task_id: str):
        """Mark task as complete"""
        mem = self.memory.get(task_id)
        if mem:
            metadata = mem.get("metadata", {})
            metadata["status"] = "completed"
            metadata["completed_at"] = datetime.now().isoformat()
            self.memory.update(task_id, metadata=metadata)
    
    def get_pending(self) -> list:
        """Get pending tasks"""
        pending = []
        
        for mem in self.memory.get_all():
            meta = mem.get("metadata", {})
            
            if meta.get("_task") and meta.get("status") == "pending":
                pending.append(mem)
        
        # Sort by priority
        pending.sort(key=lambda m: m.get("metadata", {}).get("priority", 0), reverse=True)
        return pending
    
    def get_completed(self, limit: int = 10) -> list:
        """Get completed tasks"""
        completed = []
        
        for mem in self.memory.get_all():
            meta = mem.get("metadata", {})
            
            if meta.get("_task") and meta.get("status") == "completed":
                completed.append(mem)
        
        return completed[:limit]
    
    def get_overdue(self) -> list:
        """Get overdue tasks"""
        now = datetime.now()
        overdue = []
        
        for mem in self.memory.get_all():
            meta = mem.get("metadata", {})
            
            if meta.get("_task") and meta.get("status") == "pending":
                due = meta.get("due")
                
                if due:
                    due_date = datetime.fromisoformat(due)
                    
                    if due_date < now:
                        overdue.append(mem)
        
        return overdue


def demo():
    """Demo task tracker"""
    memory = Memory(storage="json", path="./task_demo.json")
    tracker = TaskTracker(memory)
    
    print("=== Task Tracker Demo ===\n")
    
    # Add tasks
    tracker.add_task("Review PR #123", priority=4)
    tracker.add_task("Write documentation", priority=2)
    tracker.add_task("Fix critical bug", priority=5)
    tracker.add_task("Update dependencies", priority=1)
    
    print("Added 4 tasks\n")
    
    # Get pending
    print("Pending tasks:")
    for task in tracker.get_pending():
        p = task.get("metadata", {}).get("priority")
        print(f"  [{p}] {task.get('content')}")
    
    # Complete one
    pending = tracker.get_pending()
    if pending:
        tracker.complete_task(pending[0]["id"])
        print(f"\nCompleted: {pending[0]['content']}")
    
    # Show remaining
    print(f"\nRemaining: {len(tracker.get_pending())} tasks")
    
    # Cleanup
    import os
    if os.path.exists("./task_demo.json"):
        os.remove("./task_demo.json")


if __name__ == "__main__":
    demo()
