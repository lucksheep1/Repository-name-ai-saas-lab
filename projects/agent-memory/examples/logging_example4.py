"""
Memory logging_example4
logging_example4
"""
import logging


def demo():
    logger = logging.getLogger("test")
    logger.error("error message")


if __name__ == "__main__":
    demo()
