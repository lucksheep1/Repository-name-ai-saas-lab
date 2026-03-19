"""
Memory configparser_example6
configparser_example6
"""
import configparser


def demo():
    c = configparser.ConfigParser()
    c["DEFAULT"] = {"timeout": "20"}
    c["server"] = {"host": "localhost"}
    print(c.sections())


if __name__ == "__main__":
    demo()
