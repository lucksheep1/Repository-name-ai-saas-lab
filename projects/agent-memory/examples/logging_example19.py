"""
Memory logging_example19
logging_example19
"""
import logging


def demo():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("test")


if __name__ == "__main__":
    demo()
