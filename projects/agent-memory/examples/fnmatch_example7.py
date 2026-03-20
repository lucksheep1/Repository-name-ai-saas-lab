"""
Memory fnmatch_example7
fnmatch_example7
"""
import fnmatch


def demo():
    print(fnmatch.filter(["file1.txt", "file2.py", "data.csv"], "*.txt"))


if __name__ == "__main__":
    demo()
