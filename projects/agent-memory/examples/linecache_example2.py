"""
Memory linecache_example2
linecache_example2
"""
import linecache


def demo():
    linecache.getlines("/etc/hostname")


if __name__ == "__main__":
    demo()
