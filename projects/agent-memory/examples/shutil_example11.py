"""
Memory shutil_example11
shutil_example11
"""
import shutil
import os


def demo():
    if not os.path.exists("/tmp/test_dir"):
        os.makedirs("/tmp/test_dir")
    shutil.copytree("/tmp/test_dir", "/tmp/test_dir_backup")
    print("Copied")


if __name__ == "__main__":
    demo()
