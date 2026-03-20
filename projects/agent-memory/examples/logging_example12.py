"""
Memory logging_example12
logging_example12
"""
import logging


def demo():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("This is an info message")


if __name__ == "__main__":
    demo()
