"""
Memory Batch
Batch operations
"""
from memory import Memory


class Batch:
    @staticmethod
    def batch_add(memory, items: list):
        results = []
        for item in items:
            results.append(memory.add(item))
        return results


def demo():
    print("Batch ready")


if __name__ == "__main__":
    demo()
