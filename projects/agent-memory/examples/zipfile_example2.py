"""
Memory zipfile_example2
zipfile_example2
"""
import zipfile


def demo():
    with zipfile.ZipFile("data.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("test.txt", "hello world")
    print("zip created")


if __name__ == "__main__":
    demo()
