"""
Memory configparser_example2
configparser_example2
"""
import configparser


def demo():
    config = configparser.ConfigParser()
    config.read_string("""
[section1]
key1 = value1
key2 = 123
""")
    print(config["section1"]["key1"])


if __name__ == "__main__":
    demo()
