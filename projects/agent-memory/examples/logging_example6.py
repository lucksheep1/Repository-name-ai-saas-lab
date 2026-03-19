"""
Memory logging_example6
logging_example6
"""
import logging


def demo():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.warning("warning message")


if __name__ == "__main__":
    demo()
