"""
Memory yaml_example4
yaml_example4
"""
import yaml


def demo():
    data = {"key": "value", "list": [1, 2, 3]}
    print(yaml.dump(data, default_flow_style=True))


if __name__ == "__main__":
    demo()
