"""
Memory gzip_example9
gzip_example9
"""
import gzip


def demo():
    import io
    bio = io.BytesIO()
    with gzip.GzipFile(fileobj=bio, mode="w") as g:
        g.write(b"compress this")
    print(bio.getvalue()[:10])


if __name__ == "__main__":
    demo()
