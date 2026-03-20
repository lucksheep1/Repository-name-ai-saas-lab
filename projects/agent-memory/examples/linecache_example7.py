"""
Memory linecache_example7
linecache_example7
"""
import linecache


def demo():
    import sys
    sys.path.insert(0, ".")
    print(linecache.getlines("test.py"))


if __name__ == "__main__":
    demo()
