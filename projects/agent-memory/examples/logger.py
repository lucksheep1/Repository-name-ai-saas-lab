"""
Memory Logging
Structured logging with memory
"""
from agent_memory import Memory
from datetime import datetime


class MemoryLogger:
    """Memory-backed logging"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def log(self, level: str, message: str, **kwargs):
        """Log a message"""
        content = f"[{level.upper()}] {message}"
        
        tags = ["log", level.lower()]
        
        if level == "error":
            tags.append("bug")
        
        self.memory.add(
            content,
            tags=tags,
            metadata={
                "logger": True,
                **kwargs
            }
        )
    
    def info(self, message: str, **kwargs):
        self.log("info", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.log("warning", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log("error", message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self.log("debug", message, **kwargs)


class AuditLog:
    """Audit trail for actions"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def record(self, action: str, user: str = None, details: dict = None):
        """Record an audit event"""
        content = f"Action: {action}"
        
        if user:
            content += f" | User: {user}"
        
        self.memory.add(
            content,
            tags=["audit", action.lower().replace(" ", "_")],
            metadata={
                "audit": True,
                "user": user,
                "details": details or {}
            }
        )


def demo():
    """Demo logging"""
    memory = Memory(storage="json", path="./log_demo.json")
    logger = MemoryLogger(memory)
    audit = AuditLog(memory)
    
    print("=== Memory Logging Demo ===\n")
    
    # Log messages
    logger.info("Application started")
    logger.warning("High memory usage")
    logger.error("Failed to connect to database")
    
    # Audit trail
    audit.record("user.login", user="alice", details={"ip": "192.168.1.1"})
    audit.record("user.logout", user="alice")
    audit.record("data.export", user="bob", details={"records": 1000})
    
    print("Logs:")
    for m in memory.get_all():
        print(f"  [{m.get('tags', [])}] {m.get('content')}")
    
    # Cleanup
    import os
    if os.path.exists("./log_demo.json"):
        os.remove("./log_demo.json")


if __name__ == "__main__":
    demo()
