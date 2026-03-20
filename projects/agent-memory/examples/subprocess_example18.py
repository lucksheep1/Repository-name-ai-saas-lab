"""
Memory subprocess_example18
subprocess_example18
"""
import subprocess


def demo():
    result = subprocess.run(["python3", "-c", "print(1+1)"], capture_output=True)
    print(result.stdout.decode().strip())


if __name__ == "__main__":
    demo()
