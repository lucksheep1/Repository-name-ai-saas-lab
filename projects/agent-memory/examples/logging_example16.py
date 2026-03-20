"""
Memory logging_example16
logging_example16
"""
import logging


def demo():
    logging.basicConfig(level=logging.INFO)
    logging.info("Test")


if __name__ == "__main__":
    demo()
