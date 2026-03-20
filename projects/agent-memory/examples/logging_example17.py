"""
Memory logging_example17
logging_example17
"""
import logging


def demo():
    logging.basicConfig(format="%(levelname)s: %(message)s")
    logging.debug("debug")
    logging.info("info")


if __name__ == "__main__":
    demo()
