"""
Memory subprocess_example2
subprocess_example2
"""
import subprocess


def demo():
    result = subprocess.run(["python3", "-c", "print('hello')"], capture_output=True, text=True)
    print(result.stdout)


if __name__ == "__main__":
    demo()
