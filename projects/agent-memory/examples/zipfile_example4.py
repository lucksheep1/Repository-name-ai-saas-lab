"""
Memory zipfile_example4
zipfile_example4
"""
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "w") as zf:
        pass
    with zipfile.ZipFile("test.zip", "r") as zf:
        print(zf.namelist())


if __name__ == "__main__":
    demo()
