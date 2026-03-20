"""
Memory logging_example18
logging_example18
"""
import logging


def demo():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.warning("Warning")


if __name__ == "__main__":
    demo()
