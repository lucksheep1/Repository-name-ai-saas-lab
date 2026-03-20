"""
Memory configparser_example10
configparser_example10
"""
import configparser


def demo():
    c = configparser.ConfigParser()
    c["DEFAULT"] = {"ServerAliveInterval": "45"}
    c["ssh"] = {"Host": "example.com"}
    for section in c.sections():
        print(section)


if __name__ == "__main__":
    demo()
