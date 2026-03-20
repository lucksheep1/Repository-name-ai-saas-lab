"""
Memory subprocess_example14
subprocess_example14
"""
import subprocess


def demo():
    result = subprocess.run(["echo", "Hello from subprocess"], capture_output=True, text=True)
    print(result.stdout.strip())


if __name__ == "__main__":
    demo()
