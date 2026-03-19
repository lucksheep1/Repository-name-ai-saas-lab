"""
Memory Notifications
Send notifications based on memory events
"""
from agent_memory import Memory
from typing import Callable, List


class NotificationManager:
    """Manage notifications based on memory"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.handlers = []  # [(condition, handler)]
    
    def register(self, condition: Callable, handler: Callable):
        """Register notification handler"""
        self.handlers.append((condition, handler))
    
    def check_and_notify(self, mem_id: str = None):
        """Check memories and send notifications"""
        if mem_id:
            mems = [self.memory.get(mem_id)]
        else:
            mems = self.memory.get_all()
        
        notified = []
        
        for mem in mems:
            for condition, handler in self.handlers:
                try:
                    if condition(mem):
                        handler(mem)
                        notified.append(mem["id"])
                except Exception as e:
                    print(f"Notification error: {e}")
        
        return notified


# Example handlers
def email_handler(mem):
    """Send email notification"""
    print(f"📧 Email: {mem.get('content', '')[:50]}")


def slack_handler(mem):
    """Send Slack notification"""
    print(f"💬 Slack: {mem.get('content', '')[:50]}")


def webhook_handler(mem):
    """Send webhook notification"""
    print(f"🌐 Webhook: {mem.get('content', '')[:50]}")


# Example conditions
def urgent_condition(mem) -> bool:
    """Check if memory is urgent"""
    tags = mem.get("tags", [])
    priority = mem.get("priority", 0)
    
    return "urgent" in tags or priority >= 4


def bug_condition(mem) -> bool:
    """Check if memory is bug-related"""
    tags = mem.get("tags", [])
    content = mem.get("content", "").lower()
    
    return "bug" in tags or "error" in content or "exception" in content


def feedback_condition(mem) -> bool:
    """Check if memory is feedback"""
    return "feedback" in mem.get("tags", [])


class AlertRule:
    """Reusable alert rule"""
    
    def __init__(self, name: str, condition: Callable, handler: Callable, 
                 cooldown: int = 3600):
        self.name = name
        self.condition = condition
        self.handler = handler
        self.cooldown = cooldown
        self.last_triggered = {}
    
    def should_trigger(self, mem) -> bool:
        """Check if should trigger (respects cooldown)"""
        mem_id = mem.get("id", "")
        
        if mem_id in self.last_triggered:
            import time
            elapsed = time.time() - self.last_triggered[mem_id]
            if elapsed < self.cooldown:
                return False
        
        return self.condition(mem)
    
    def trigger(self, mem):
        """Trigger the handler"""
        self.handler(mem)
        
        import time
        mem_id = mem.get("id", "")
        self.last_triggered[mem_id] = time.time()


def demo():
    """Demo notifications"""
    memory = Memory(storage="json", path="./notify_demo.json")
    manager = NotificationManager(memory)
    
    print("=== Notification Manager Demo ===\n")
    
    # Register handlers
    manager.register(urgent_condition, email_handler)
    manager.register(bug_condition, slack_handler)
    manager.register(feedback_condition, webhook_handler)
    
    # Add memories
    memory.add("Normal conversation", tags=["chat"])
    memory.add("Critical: System down!", tags=["urgent"], priority=5)
    memory.add("Bug in payment", tags=["bug"])
    memory.add("User feedback: love it!", tags=["feedback"])
    
    print("Added 4 memories with different types\n")
    
    # Check and notify
    print("Notifications:")
    manager.check_and_notify()
    
    # Cleanup
    import os
    if os.path.exists("./notify_demo.json"):
        os.remove("./notify_demo.json")


if __name__ == "__main__":
    demo()
