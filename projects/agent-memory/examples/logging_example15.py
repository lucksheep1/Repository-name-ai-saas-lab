"""
Memory logging_example15
logging_example15
"""
import logging


def demo():
    logger = logging.getLogger("test")
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
    logger.warning("Warning message")


if __name__ == "__main__":
    demo()
