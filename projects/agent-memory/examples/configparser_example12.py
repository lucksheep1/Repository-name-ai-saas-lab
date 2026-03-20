"""
Memory configparser_example12
configparser_example12
"""
import configparser


def demo():
    c = configparser.ConfigParser()
    c["DEFAULT"] = {"debug": "true"}
    c["section1"] = {}
    print(c.has_option("section1", "debug"))


if __name__ == "__main__":
    demo()
