"""
Memory shutil_example10
shutil_example10
"""
import shutil


def demo():
    print(shutil.make_archive("archive", "zip", ".", "."))


if __name__ == "__main__":
    demo()
