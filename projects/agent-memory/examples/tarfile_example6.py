"""
Memory tarfile_example6
tarfile_example6
"""
import tarfile


def demo():
    with tarfile.open("test.tar", "r") as t:
        print(t.getnames())


if __name__ == "__main__":
    demo()
