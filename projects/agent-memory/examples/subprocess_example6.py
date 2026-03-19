"""
Memory subprocess_example6
subprocess_example6
"""
import subprocess


def demo():
    result = subprocess.run(["python3", "-c", "print(1+1)"], capture_output=True, text=True)
    print(result.stdout)


if __name__ == "__main__":
    demo()
