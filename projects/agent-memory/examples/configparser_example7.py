"""
Memory configparser_example7
configparser_example7
"""
import configparser


def demo():
    c = configparser.ConfigParser()
    c.read_string("[DEFAULT]\nserver=localhost")
    print(c.get("DEFAULT", "server"))


if __name__ == "__main__":
    demo()
