"""
Memory tarfile_example3
tarfile_example3
"""
import tarfile


def demo():
    with tarfile.open("test.tar.gz", "w:gz") as tf:
        import io
        data = io.BytesIO(b"file content")
        info = tarfile.TarInfo(name="file.txt")
        info.size = len(data.getvalue())
        tf.addfile(info, data)


if __name__ == "__main__":
    demo()
