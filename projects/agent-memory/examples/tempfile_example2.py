"""
Memory tempfile_example2
tempfile_example2
"""
import tempfile


def demo():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        print(tf.name)


if __name__ == "__main__":
    demo()
