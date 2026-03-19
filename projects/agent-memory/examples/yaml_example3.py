"""
Memory yaml_example3
yaml_example3
"""
import yaml


def demo():
    data = {"list": [1, 2, 3], "dict": {"a": 1}}
    yaml_str = yaml.dump(data, default_flow_style=False)
    parsed = yaml.safe_load(yaml_str)
    print(parsed)


if __name__ == "__main__":
    demo()
