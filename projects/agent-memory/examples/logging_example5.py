"""
Memory logging_example5
logging_example5
"""
import logging


def demo():
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    logging.debug("debug message")
    logging.info("info message")


if __name__ == "__main__":
    demo()
