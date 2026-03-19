"""
Memory linecache_example3
linecache_example3
"""
import linecache


def demo():
    print(linecache.getlines("/etc/hostname"))


if __name__ == "__main__":
    demo()
