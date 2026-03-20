"""
Memory tarfile_example9
tarfile_example9
"""
import tarfile


def demo():
    with tarfile.open("test.tar", "w:gz") as tar:
        import io
        info = tarfile.TarInfo(name="test.txt")
        info.size = 6
        tar.addfile(info, io.BytesIO(b"hello"))


if __name__ == "__main__":
    demo()
