"""
Memory Profiler
Profile memory operations
"""
from memory import Memory


class Profiler:
    def __init__(self):
        self.timings = {}
    
    def time(self, name: str):
        import time
        start = time.time()
        return lambda: self.timings.update({name: time.time() - start})


def demo():
    profiler = Profiler()
    end = profiler.time("test")
    end()
    print(profiler.timings)


if __name__ == "__main__":
    demo()
