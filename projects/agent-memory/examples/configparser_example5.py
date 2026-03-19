"""
Memory configparser_example5
configparser_example5
"""
import configparser


def demo():
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"key": "value"}
    print("DEFAULT" in config)


if __name__ == "__main__":
    demo()
