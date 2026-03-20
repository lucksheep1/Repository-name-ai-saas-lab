"""
Memory gzip_example6
gzip_example6
"""
import gzip


def demo():
    import io
    with gzip.GzipFile(fileobj=io.BytesIO(b"test"), mode="r") as g:
        print(g.read())


if __name__ == "__main__":
    demo()
