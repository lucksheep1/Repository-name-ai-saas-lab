"""
Memory linecache_example10
linecache_example10
"""
import linecache


def demo():
    print(linecache.getlines("/etc/passwd")[:1])


if __name__ == "__main__":
    demo()
