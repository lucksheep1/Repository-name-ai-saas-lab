"""
Memory linecache_example7
linecache_example7
"""
import linecache


def demo():
    lines = linecache.getlines("/etc/hostname")
    print(len(lines))


if __name__ == "__main__":
    demo()
