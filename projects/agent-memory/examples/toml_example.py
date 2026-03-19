"""
Memory toml_example
toml_example
"""
import toml


def demo():
    print(toml.dumps({"section": {"key": "value"}}))


if __name__ == "__main__":
    demo()
