"""
Memory fnmatch_example8
fnmatch_example8
"""
import fnmatch


def demo():
    names = ["test.py", "test.txt", "data.csv", "main.py"]
    py_files = fnmatch.filter(names, "*.py")
    print(py_files)


if __name__ == "__main__":
    demo()
