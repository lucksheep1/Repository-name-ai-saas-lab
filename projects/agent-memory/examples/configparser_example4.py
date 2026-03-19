"""
Memory configparser_example4
configparser_example4
"""
import configparser


def demo():
    config = configparser.ConfigParser()
    config["DEFAULT"] = {" Compression ": "yes"}
    print(config["DEFAULT"]["compression"])


if __name__ == "__main__":
    demo()
