"""
Memory json_example14
json_example14
"""
import json


def demo():
    data = {"name": "Alice", "skills": ["Python", "AI"]}
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    demo()
