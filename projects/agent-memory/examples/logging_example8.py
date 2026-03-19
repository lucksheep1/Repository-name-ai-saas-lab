"""
Memory logging_example8
logging_example8
"""
import logging


def demo():
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.debug("debug message")


if __name__ == "__main__":
    demo()
