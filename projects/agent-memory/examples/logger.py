"""
Memory Logger
Integrate with Python logging
"""
from agent_memory import Memory
import logging
import sys


class MemoryHandler(logging.Handler):
    """Logging handler that stores in memory"""
    
    def __init__(self, memory: Memory, level: int = logging.INFO):
        super().__init__(level)
        self.memory = memory
    
    def emit(self, record: logging.LogRecord):
        """Store log record in memory"""
        try:
            msg = self.format(record)
            
            # Determine tags from level
            tags = ["log"]
            if record.levelno >= logging.ERROR:
                tags.append("error")
            elif record.levelno >= logging.WARNING:
                tags.append("warning")
            
            self.memory.add(msg, tags=tags)
        except Exception:
            self.handleError(record)


def setup_logging(memory: Memory, level: int = logging.INFO):
    """Setup logging to memory"""
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Add memory handler
    handler = MemoryHandler(memory, level)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    logger.addHandler(handler)
    
    return logger


def demo():
    """Demo logging"""
    memory = Memory(storage="json", path="./logging_demo.json")
    
    print("=== Memory Logger Demo ===\n")
    
    # Setup
    logger = setup_logging(memory)
    
    # Log messages
    logger.info("Application started")
    logger.warning("This is a warning")
    logger.error("An error occurred")
    
    # Also use standard print
    logger.info("User logged in")
    
    print("Logged 4 messages\n")
    
    # Show memories
    for mem in memory.get_all():
        print(f"[{mem.get('tags')}] {mem.get('content')[:60]}")
    
    # Cleanup
    import os
    if os.path.exists("./logging_demo.json"):
        os.remove("./logging_demo.json")


if __name__ == "__main__":
    demo()
