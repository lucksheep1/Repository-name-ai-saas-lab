"""
Memory gzip_example5
gzip_example5
"""
import gzip


def demo():
    import io
    with gzip.GzipFile(fileobj=io.BytesIO(), mode="w") as g:
        g.write(b"hello world")


if __name__ == "__main__":
    demo()
