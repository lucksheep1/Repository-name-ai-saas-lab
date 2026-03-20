"""
Memory tarfile_example12
tarfile_example12
"""
import tarfile


def demo():
    with tarfile.open("test.tar", "r") as t:
        print(t.getmembers())


if __name__ == "__main__":
    demo()
