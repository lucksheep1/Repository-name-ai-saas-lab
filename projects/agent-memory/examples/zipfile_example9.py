"""
Memory zipfile_example9
zipfile_example9
"""
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "w") as z:
        z.writestr("hello.txt", "Hello World!")
        print(z.namelist())


if __name__ == "__main__":
    demo()
