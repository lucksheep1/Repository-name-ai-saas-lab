"""
Memory linecache_example8
linecache_example8
"""
import linecache


def demo():
    linecache.cache.clear()
    print("Cache cleared")


if __name__ == "__main__":
    demo()
