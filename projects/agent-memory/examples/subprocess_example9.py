"""
Memory subprocess_example9
subprocess_example9
"""
import subprocess


def demo():
    result = subprocess.run(["python3", "-c", "print('hello')"], capture_output=True, text=True)
    print(result.stdout)


if __name__ == "__main__":
    demo()
