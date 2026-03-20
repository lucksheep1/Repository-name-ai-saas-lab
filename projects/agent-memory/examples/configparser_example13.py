"""
Memory configparser_example13
configparser_example13
"""
import configparser


def demo():
    c = configparser.ConfigParser()
    c["section"] = {"key": "value"}
    print(c.sections())


if __name__ == "__main__":
    demo()
