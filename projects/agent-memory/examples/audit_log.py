"""
Memory Audit Log
Audit memory access
"""
from agent_memory import Memory
import time


class AuditLog:
    """Audit log"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.log = []
    
    def log_action(self, action: str, user: str, details: str = ""):
        """Log action"""
        entry = {
            "action": action,
            "user": user,
            "details": details,
            "timestamp": time.time()
        }
        
        self.log.append(entry)
        
        # Also store in memory
        self.memory.add(
            f"[AUDIT] {user} {action} {details}",
            tags=["audit", action]
        )
    
    def get_log(self, user: str = None, action: str = None):
        """Get audit log"""
        results = self.log
        
        if user:
            results = [e for e in results if e["user"] == user]
        
        if action:
            results = [e for e in results if e["action"] == action]
        
        return results


def demo():
    """Demo audit"""
    memory = Memory(storage="json", path="./audit_demo.json")
    audit = AuditLog(memory)
    
    audit.log_action("add", "alice", "Added memory")
    audit.log_action("search", "bob", "Searched test")
    
    print("Audit:", len(audit.get_log()))
    
    import os
    if os.path.exists("./audit_demo.json"):
        os.remove("./audit_demo.json")


if __name__ == "__main__":
    demo()
