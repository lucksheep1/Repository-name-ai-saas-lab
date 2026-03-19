"""
Memory logging_example3
logging_example3
"""
import logging


def demo():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    print(handler)


if __name__ == "__main__":
    demo()
