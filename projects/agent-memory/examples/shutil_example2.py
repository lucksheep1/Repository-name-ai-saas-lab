"""
Memory shutil_example2
shutil_example2
"""
import shutil


def demo():
    print(shutil.make_archive("archive", "zip", ".", "."))


if __name__ == "__main__":
    demo()
