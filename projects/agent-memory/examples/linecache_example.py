"""
Memory linecache_example
linecache_example
"""
import linecache


def demo():
    print(linecache.getlines("/etc/hostname")[:1])


if __name__ == "__main__":
    demo()
