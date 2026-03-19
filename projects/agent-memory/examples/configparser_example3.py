"""
Memory configparser_example3
configparser_example3
"""
import configparser


def demo():
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"ServerAliveInterval": "45", "Compression": "yes"}
    config["github.com"] = {}
    config["github.com"]["User"] = "hg"
    import io
    output = io.StringIO()
    config.write(output)
    print(output.getvalue()[:50])


if __name__ == "__main__":
    demo()
