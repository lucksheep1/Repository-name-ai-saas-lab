"""
Memory subprocess_example20
subprocess_example20
"""
import subprocess


def demo():
    result = subprocess.run(["echo", "hello"], capture_output=True, text=True)
    print(result.stdout.strip())


if __name__ == "__main__":
    demo()
