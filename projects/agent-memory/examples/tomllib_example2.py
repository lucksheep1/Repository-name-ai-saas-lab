"""
Memory tomllib_example2
tomllib_example2
"""
import tomllib


def demo():
    toml_str = """
[project]
name = "test"
version = "1.0"
"""
    data = tomllib.loads(toml_str)
    print(data["project"]["name"])


if __name__ == "__main__":
    demo()
