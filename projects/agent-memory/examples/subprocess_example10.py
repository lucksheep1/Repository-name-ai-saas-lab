"""
Memory subprocess_example10
subprocess_example10
"""
import subprocess


def demo():
    result = subprocess.run(["ls", "-1"], capture_output=True, text=True)
    print(len(result.stdout.splitlines()))


if __name__ == "__main__":
    demo()
