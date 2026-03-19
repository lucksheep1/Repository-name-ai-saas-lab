"""
Memory logging_example7
logging_example7
"""
import logging


def demo():
    logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("myapp")
    logger.info("info message")


if __name__ == "__main__":
    demo()
