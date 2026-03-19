"""
Memory tarfile_example2
tarfile_example2
"""
import tarfile


def demo():
    with tarfile.open("data.tar", "w") as tf:
        import io
        info = tarfile.TarInfo("test.txt")
        info.size = 11
        tf.addfile(info, io.BytesIO(b"hello world"))
    print("tar created")


if __name__ == "__main__":
    demo()
