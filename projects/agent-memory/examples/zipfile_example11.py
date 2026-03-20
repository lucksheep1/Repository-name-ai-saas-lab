"""
Memory zipfile_example11
zipfile_example11
"""
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "w") as z:
        z.writestr("test.txt", "content")
        print(z.getinfo("test.txt").file_size)


if __name__ == "__main__":
    demo()
