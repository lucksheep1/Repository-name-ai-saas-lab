"""
Memory tarfile_example4
tarfile_example4
"""
import tarfile


def demo():
    with tarfile.open("test.tar", "w") as tf:
        pass
    with tarfile.open("test.tar", "r") as tf:
        print(len(tf.getmembers()))


if __name__ == "__main__":
    demo()
