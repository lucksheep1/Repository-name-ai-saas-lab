"""
Memory Scheduler
Schedule memory operations at specific times
"""
from agent_memory import Memory
import time
from datetime import datetime, timedelta
from threading import Thread


class MemoryScheduler:
    """Schedule memory operations"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.scheduled = []  # [(timestamp, callback, args)]
        self.running = False
    
    def schedule(self, timestamp: float, callback: callable, *args):
        """Schedule a callback"""
        self.scheduled.append((timestamp, callback, args))
    
    def schedule_in(self, seconds: float, callback: callable, *args):
        """Schedule callback in N seconds"""
        timestamp = time.time() + seconds
        self.schedule(timestamp, callback, args)
    
    def run(self, check_interval: float = 1.0):
        """Run scheduler (blocking)"""
        self.running = True
        
        while self.running:
            now = time.time()
            
            # Check due callbacks
            due = [(ts, cb, args) for ts, cb, args in self.scheduled if ts <= now]
            
            for ts, cb, args in due:
                try:
                    cb(*args)
                except Exception as e:
                    print(f"Scheduler error: {e}")
                self.scheduled.remove((ts, cb, args))
            
            time.sleep(check_interval)
    
    def start_daemon(self):
        """Start scheduler in background thread"""
        thread = Thread(target=self.run, daemon=True)
        thread.start()
    
    def stop(self):
        """Stop scheduler"""
        self.running = False


class Reminder:
    """Memory-based reminders"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def add_reminder(self, content: str, remind_at: str):
        """Add a reminder
        
        Args:
            content: What to remember
            remind_at: ISO timestamp or relative (e.g., "+1h", "2026-03-20 10:00")
        """
        # Parse time
        if remind_at.startswith("+"):
            # Relative time
            value = int(remind_at[1:-1])
            unit = remind_at[-1]
            
            if unit == "m":
                delta = timedelta(minutes=value)
            elif unit == "h":
                delta = timedelta(hours=value)
            elif unit == "d":
                delta = timedelta(days=value)
            else:
                delta = timedelta(seconds=value)
            
            remind_time = datetime.now() + delta
        else:
            remind_time = datetime.fromisoformat(remind_at)
        
        # Store with metadata
        self.memory.add(
            content,
            metadata={
                "_reminder": True,
                "remind_at": remind_time.isoformat()
            }
        )
    
    def get_due(self) -> list:
        """Get due reminders"""
        now = datetime.now()
        due = []
        
        for mem in self.memory.get_all():
            meta = mem.get("metadata", {})
            
            if meta.get("_reminder"):
                remind_at = meta.get("remind_at")
                if remind_at:
                    remind_time = datetime.fromisoformat(remind_at)
                    if remind_time <= now:
                        due.append(mem)
        
        return due
    
    def clear_old(self) -> int:
        """Clear old reminders"""
        now = datetime.now()
        cleared = 0
        
        for mem in self.memory.get_all():
            meta = mem.get("metadata", {})
            
            if meta.get("_reminder"):
                remind_at = meta.get("remind_at")
                if remind_at:
                    remind_time = datetime.fromisoformat(remind_at)
                    if remind_time <= now:
                        self.memory.forget(mem["id"])
                        cleared += 1
        
        return cleared


def demo():
    """Demo scheduler"""
    memory = Memory(storage="json", path="./scheduler_demo.json")
    scheduler = MemoryScheduler(memory)
    reminder = Reminder(memory)
    
    print("=== Memory Scheduler Demo ===\n")
    
    # Add reminders
    reminder.add_reminder("Meeting at 3pm", "+1m")  # Due in 1 minute
    reminder.add_reminder("Call mom", "+2m")
    reminder.add_reminder("Review PR", "+5m")
    
    print("Added 3 reminders (will be due soon)")
    
    # Check immediately (won't be due yet)
    due = reminder.get_due()
    print(f"Due now: {len(due)}")
    
    # Show scheduled
    print(f"Scheduled tasks: {len(scheduler.scheduled)}")
    
    # Cleanup
    import os
    if os.path.exists("./scheduler_demo.json"):
        os.remove("./scheduler_demo.json")


if __name__ == "__main__":
    demo()
