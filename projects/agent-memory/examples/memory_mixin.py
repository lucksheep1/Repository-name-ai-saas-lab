"""
Memory Mixin
Mixin pattern
"""
from memory import Memory


class LoggingMixin:
    def log(self, msg: str):
        print(f"LOG: {msg}")


class MixinMemory(LoggingMixin, Memory):
    pass


def demo():
    mem = MixinMemory(storage="json", path="test.json")
    mem.log("Test")
    print(mem.add("Hello"))


if __name__ == "__main__":
    demo()
