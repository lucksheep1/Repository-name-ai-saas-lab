"""
Memory logging_example13
logging_example13
"""
import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.msg = f"[CUSTOM] {record.msg}"
        return super().format(record)


def demo():
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter("%(message)s"))
    logger = logging.getLogger("custom")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info("Test message")


if __name__ == "__main__":
    demo()
