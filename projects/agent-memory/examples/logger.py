#!/usr/bin/env python3
"""
Agent Memory - Memory Logger
===========================
Structured logging with memory.

Usage:
    from logger import AgentLogger
    
    logger = AgentLogger()
    logger.info("User logged in")
    logger.error("Failed to connect")
    logger.warning("Low memory")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional
from agent_memory import Memory


class AgentLogger:
    """Structured logger with memory."""
    
    LEVELS = {
        "DEBUG": 1,
        "INFO": 2,
        "WARNING": 3,
        "ERROR": 4,
        "CRITICAL": 5
    }
    
    def __init__(self, storage: str = "json", path: str = "./memory.json", min_level: str = "INFO"):
        self.memory = Memory(storage=storage, path=path)
        self.min_level = self.LEVELS.get(min_level.upper(), 2)
    
    def _log(self, level: str, message: str, metadata: dict = None):
        """Log a message."""
        level_num = self.LEVELS.get(level.upper(), 2)
        
        if level_num < self.min_level:
            return
        
        # Format message
        formatted = f"[{level.upper()}] {message}"
        
        # Add to memory with tags
        tags = [level.lower(), "log"]
        
        metadata = metadata or {}
        metadata["level"] = level.upper()
        
        self.memory.add(formatted, tags=tags, metadata=metadata)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log("DEBUG", message, kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log("INFO", message, kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log("WARNING", message, kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log("ERROR", message, kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log("CRITICAL", message, kwargs)
    
    def get_logs(self, level: str = None, limit: int = 50):
        """Get logs."""
        if level:
            return self.memory.get_by_tag(level.lower())
        return self.memory.get_recent(limit=limit)
    
    def get_errors(self, limit: int = 20):
        """Get error logs."""
        return self.memory.get_by_tag("error")


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "logger_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Logger Demo")
    print("=" * 50)
    
    # Create logger
    logger = AgentLogger(storage="json", path=demo_path)
    
    # Log messages
    print("\n1. Logging messages...")
    logger.info("Application started")
    logger.info("User logged in", user_id=123)
    logger.warning("High memory usage", usage="85%")
    logger.error("Database connection failed", error="timeout")
    logger.info("Processing request", request_id="abc123")
    logger.error("API call failed", status=500)
    logger.critical("System shutdown")
    
    print("   Logged 7 messages")
    
    # Get all logs
    print("\n2. All logs:")
    logs = logger.get_logs(limit=10)
    for log in logs:
        level = log.get("metadata", {}).get("level", "INFO")
        print(f"   {level}: {log['text']}")
    
    # Get errors
    print("\n3. Errors only:")
    errors = logger.get_errors()
    for err in errors:
        print(f"   {err['text']}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
