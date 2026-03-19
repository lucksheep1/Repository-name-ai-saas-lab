"""
Memory fnmatch_example3
fnmatch_example3
"""
import fnmatch


def demo():
    names = ["file1.txt", "file2.py", "file3.md"]
    print(fnmatch.filter(names, "*.txt"))


if __name__ == "__main__":
    demo()
