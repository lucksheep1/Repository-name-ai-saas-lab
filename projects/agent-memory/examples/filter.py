"""
Memory Filter
Filter memories
"""
from memory import Memory


class Filter:
    @staticmethod
    def filter_by_content(memory, min_length: int = 5):
        return [m for m in memory.get_all() 
                if len(m.get("content", "")) >= min_length]


def demo():
    print("Filter ready")


if __name__ == "__main__":
    demo()
