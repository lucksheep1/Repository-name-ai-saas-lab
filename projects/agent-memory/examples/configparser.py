"""
Memory ConfigParser
Config parser
"""
from memory import Memory
import configparser


def demo():
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"key": "value"}
    print(config["DEFAULT"]["key"])


if __name__ == "__main__":
    demo()
