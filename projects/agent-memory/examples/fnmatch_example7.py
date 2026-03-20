"""
Memory fnmatch_example7
fnmatch_example7
"""
import fnmatch


def demo():
    files = ["test.py", "test.txt", "main.py", "data.csv"]
    print([f for f in files if fnmatch.fnmatch(f, "*.py")])


if __name__ == "__main__":
    demo()
