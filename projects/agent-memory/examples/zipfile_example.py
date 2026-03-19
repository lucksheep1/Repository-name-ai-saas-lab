"""
Memory zipfile_example
zipfile_example
"""
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "w") as zf:
        pass
    print("zip created")


if __name__ == "__main__":
    demo()
