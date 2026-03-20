"""
Memory zipfile_example12
zipfile_example12
"""
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "r") as z:
        print(z.namelist())


if __name__ == "__main__":
    demo()
