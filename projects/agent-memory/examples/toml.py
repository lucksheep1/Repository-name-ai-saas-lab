"""
Memory TOML
TOML parsing
"""
from memory import Memory
import toml


def demo():
    data = {"key": "value"}
    toml_str = toml.dumps(data)
    print(toml_str)


if __name__ == "__main__":
    demo()
