"""
Memory Formatter
Format memory data
"""
from memory import Memory


class Formatter:
    @staticmethod
    def format_text(mem: dict) -> str:
        content = mem.get("content", "")
        tags = ", ".join(mem.get("tags", []))
        return f"{content} [{tags}]"
    
    @staticmethod
    def format_html(mem: dict) -> str:
        content = mem.get("content", "")
        tags = " ".join(f'<span class="tag">{t}</span>' for t in mem.get("tags", []))
        return f'<div class="memory">{content}<div class="tags">{tags}</div></div>'


def demo():
    mem = {"content": "Test", "tags": ["a", "b"]}
    print(Formatter.format_text(mem))


if __name__ == "__main__":
    demo()
