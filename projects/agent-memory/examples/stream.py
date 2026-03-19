"""
Memory Stream
Stream operations
"""
from memory import Memory


class Stream:
    @staticmethod
    def stream(memory):
        for mem in memory.get_all():
            yield mem


def demo():
    print("Stream ready")


if __name__ == "__main__":
    demo()
