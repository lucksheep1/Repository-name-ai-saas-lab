"""
Memory configparser_example8
configparser_example8
"""
import configparser


def demo():
    c = configparser.ConfigParser()
    c["DEFAULT"] = {"key": "value"}
    import io
    s = io.StringIO()
    c.write(s)
    print(s.getvalue()[:50])


if __name__ == "__main__":
    demo()
