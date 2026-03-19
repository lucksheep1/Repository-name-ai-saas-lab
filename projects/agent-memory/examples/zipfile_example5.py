"""
Memory zipfile_example5
zipfile_example5
"""
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "w") as z:
        z.writestr("test.txt", "hello world")


if __name__ == "__main__":
    demo()
