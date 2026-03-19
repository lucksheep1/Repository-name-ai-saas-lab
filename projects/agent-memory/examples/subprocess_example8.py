"""
Memory subprocess_example8
subprocess_example8
"""
import subprocess


def demo():
    result = subprocess.run(["echo", "hello world"], capture_output=True, text=True)
    print(result.stdout.strip())


if __name__ == "__main__":
    demo()
