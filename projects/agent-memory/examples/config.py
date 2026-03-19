"""
Memory Config
Configuration
"""
from memory import Memory


class Config:
    DEBUG = True
    VERSION = "1.0"


def demo():
    print(f"Version: {Config.VERSION}")


if __name__ == "__main__":
    demo()
