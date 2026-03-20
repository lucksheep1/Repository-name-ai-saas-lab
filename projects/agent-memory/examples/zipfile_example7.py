"""
Memory zipfile_example7
zipfile_example7
"""
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "a") as z:
        z.writestr("new.txt", "content")


if __name__ == "__main__":
    demo()
