"""
Memory tarfile_example11
tarfile_example11
"""
import tarfile


def demo():
    with tarfile.open("test.tar", "w") as t:
        import io
        info = tarfile.TarInfo("test.txt")
        info.size = 4
        t.addfile(info, io.BytesIO(b"test"))


if __name__ == "__main__":
    demo()
