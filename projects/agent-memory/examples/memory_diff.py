"""
Memory Diff
Diff between memories
"""
from memory import Memory


def diff(mem1: dict, mem2: dict) -> dict:
    """Simple diff"""
    changes = {}
    
    for key in ["content", "tags"]:
        v1 = mem1.get(key, [])
        v2 = mem2.get(key, [])
        
        if v1 != v2:
            changes[key] = {"old": v1, "new": v2}
    
    return changes


def demo():
    m1 = {"content": "Hello", "tags": ["a"]}
    m2 = {"content": "Hello", "tags": ["b"]}
    
    print(f"Diff: {diff(m1, m2)}")


if __name__ == "__main__":
    demo()
