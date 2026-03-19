"""
Memory subprocess_example7
subprocess_example7
"""
import subprocess


def demo():
    result = subprocess.run(["python3", "-c", "import sys; print(sys.version)"], capture_output=True, text=True)
    print(result.stdout[:50])


if __name__ == "__main__":
    demo()
