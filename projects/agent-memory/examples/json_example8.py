"""
Memory json_example8
json_example8
"""
import json


def demo():
    data = {"name": "Alice", "skills": ["Python", "JavaScript"]}
    json_str = json.dumps(data, indent=2)
    parsed = json.loads(json_str)
    print(parsed)


if __name__ == "__main__":
    demo()
