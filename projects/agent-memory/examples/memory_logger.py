"""
Memory Logger
Logger for memory
"""
from memory import Memory


class Logger:
    def __init__(self):
        self.logs = []
    
    def info(self, msg: str):
        self.logs.append(f"INFO: {msg}")
    
    def error(self, msg: str):
        self.logs.append(f"ERROR: {msg}")


def demo():
    logger = Logger()
    logger.info("Test message")
    print(logger.logs)


if __name__ == "__main__":
    demo()
