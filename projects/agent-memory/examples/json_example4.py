"""
Memory json_example4
json_example4
"""
import json


def demo():
    data = {"name": "Alice", "age": 30, "skills": ["Python", "JS"]}
    json_str = json.dumps(data, indent=4, sort_keys=True)
    print(json_str[:50])


if __name__ == "__main__":
    demo()
