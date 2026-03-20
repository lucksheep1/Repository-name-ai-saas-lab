"""
Memory zipfile_example10
zipfile_example10
"""
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "r") as z:
        print(z.namelist()[:3])


if __name__ == "__main__":
    demo()
