"""
Memory Normalizer
Normalize memory data
"""
from memory import Memory


class Normalizer:
    @staticmethod
    def normalize_content(content: str) -> str:
        return content.strip().replace("  ", " ")
    
    @staticmethod
    def normalize_tags(tags: list) -> list:
        return sorted(set(t.strip().lower() for t in tags if t.strip()))


def demo():
    content = "  Test  1  "
    tags = ["A", "b", "C"]
    
    print(f"Content: '{Normalizer.normalize_content(content)}'")
    print(f"Tags: {Normalizer.normalize_tags(tags)}")


if __name__ == "__main__":
    demo()
