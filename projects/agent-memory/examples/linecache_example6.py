"""
Memory linecache_example6
linecache_example6
"""
import linecache


def demo():
    print(linecache.getline("/etc/hostname", 0))


if __name__ == "__main__":
    demo()
