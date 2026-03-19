"""
Memory subprocess_example4
subprocess_example4
"""
import subprocess


def demo():
    result = subprocess.run("echo test", shell=True, capture_output=True, text=True)
    print(result.stdout.strip())


if __name__ == "__main__":
    demo()
