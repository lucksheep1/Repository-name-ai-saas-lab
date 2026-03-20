"""
Memory configparser_example11
configparser_example11
"""
import configparser


def demo():
    c = configparser.ConfigParser()
    c.read_string("""
[section1]
key1 = value1
key2 = value2
""")
    print(c.get("section1", "key1"))


if __name__ == "__main__":
    demo()
