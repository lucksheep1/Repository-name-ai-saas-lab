"""
Memory tempfile_example12
tempfile_example12
"""
import tempfile


def demo():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        print(f.name)


if __name__ == "__main__":
    demo()
