"""
Memory tarfile_example5
tarfile_example5
"""
import tarfile


def demo():
    with tarfile.open("test.tar", "w") as t:
        import io
        info = tarfile.TarInfo(name="test.txt")
        info.size = 5
        t.addfile(info, io.BytesIO(b"hello"))


if __name__ == "__main__":
    demo()
