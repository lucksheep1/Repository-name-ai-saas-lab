"""
Memory zipfile_example3
zipfile_example3
"""
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "w") as zf:
        zf.writestr("readme.txt", "This is a readme")
    with zipfile.ZipFile("test.zip", "r") as zf:
        print(zf.namelist())


if __name__ == "__main__":
    demo()
