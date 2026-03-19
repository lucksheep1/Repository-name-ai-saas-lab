"""
Memory configparser_example
configparser_example
"""
import configparser


def demo():
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"debug": "true"}
    print(config["DEFAULT"]["debug"])


if __name__ == "__main__":
    demo()
