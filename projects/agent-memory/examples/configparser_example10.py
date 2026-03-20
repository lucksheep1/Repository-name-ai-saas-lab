"""
Memory configparser_example10
configparser_example10
"""
import configparser


def demo():
    c = configparser.ConfigParser()
    c["DEFAULT"] = {"key": "value"}
    c["section1"] = {"option": "data"}
    for section in c.sections():
        print(section)


if __name__ == "__main__":
    demo()
