"""
Memory logging_example
logging_example
"""
import logging


def demo():
    logging.basicConfig(level=logging.INFO)
    logging.info("test")


if __name__ == "__main__":
    demo()
