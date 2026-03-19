"""
Memory tarfile_example
tarfile_example
"""
import tarfile


def demo():
    with tarfile.open("test.tar", "w") as tf:
        pass
    print("tar created")


if __name__ == "__main__":
    demo()
