"""
Memory configparser
configparser utilities
"""
import configparser


def demo():
    c = configparser.ConfigParser()
    c["section"] = {"key": "value"}
    print(c["section"]["key"])


if __name__ == "__main__":
    demo()
