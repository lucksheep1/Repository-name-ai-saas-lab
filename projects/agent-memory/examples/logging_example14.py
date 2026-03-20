"""
Memory logging_example14
logging_example14
"""
import logging


def demo():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    logger.debug("Debug message")
    logger.info("Info message")


if __name__ == "__main__":
    demo()
