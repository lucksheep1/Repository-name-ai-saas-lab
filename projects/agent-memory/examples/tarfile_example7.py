"""
Memory tarfile_example7
tarfile_example7
"""
import tarfile


def demo():
    with tarfile.open("test.tar", "r") as t:
        print(t.getmembers())


if __name__ == "__main__":
    demo()
