"""
Memory Logging
Logging utilities
"""
from memory import Memory
import logging


def demo():
    logging.basicConfig(level=logging.INFO)
    logging.info("test")


if __name__ == "__main__":
    demo()
