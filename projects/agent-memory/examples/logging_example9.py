"""
Memory logging_example9
logging_example9
"""
import logging


def demo():
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)
    logger.warning("warning message")


if __name__ == "__main__":
    demo()
