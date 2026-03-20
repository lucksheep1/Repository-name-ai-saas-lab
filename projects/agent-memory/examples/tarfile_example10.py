"""
Memory tarfile_example10
tarfile_example10
"""
import tarfile


def demo():
    with tarfile.open("test.tar.gz", "r:gz") as tar:
        print(tar.getmembers()[:3])


if __name__ == "__main__":
    demo()
