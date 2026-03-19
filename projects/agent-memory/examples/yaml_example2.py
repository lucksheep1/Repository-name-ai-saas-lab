"""
Memory yaml_example2
yaml_example2
"""
import yaml


def demo():
    data = {"key": "value", "list": [1, 2, 3]}
    yaml_str = yaml.dump(data)
    parsed = yaml.safe_load(yaml_str)
    print(parsed)


if __name__ == "__main__":
    demo()
