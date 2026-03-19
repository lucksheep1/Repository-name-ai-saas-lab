"""
Memory YAML
YAML parsing
"""
from memory import Memory
import yaml


def demo():
    data = {"key": "value"}
    yaml_str = yaml.dump(data)
    print(yaml_str)
    
    parsed = yaml.safe_load(yaml_str)
    print(parsed)


if __name__ == "__main__":
    demo()
