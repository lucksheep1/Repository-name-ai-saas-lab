"""
Memory linecache_example9
linecache_example9
"""
import linecache


def demo():
    linecache.cache.clear()
    print("Cleared")


if __name__ == "__main__":
    demo()
