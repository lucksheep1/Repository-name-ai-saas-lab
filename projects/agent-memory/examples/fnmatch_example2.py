"""
Memory fnmatch_example2
fnmatch_example2
"""
import fnmatch


def demo():
    names = ["test.py", "test.txt", "app.py", "data.json"]
    py_files = fnmatch.filter(names, "*.py")
    print(py_files)


if __name__ == "__main__":
    demo()
