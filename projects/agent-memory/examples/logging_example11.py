"""
Memory logging_example11
logging_example11
"""
import logging


def demo():
    logging.basicConfig(format="%(levelname)s: %(message)s")
    logging.debug("debug")


if __name__ == "__main__":
    demo()
