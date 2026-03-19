"""
Memory logging_example2
logging_example2
"""
import logging


def demo():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    print(logger.level)


if __name__ == "__main__":
    demo()
