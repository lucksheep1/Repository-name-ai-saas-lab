"""
Memory argparse_example6
argparse_example6
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=argparse.FileType("r"))
    args = parser.parse_args(["--file", "/dev/null"])
    print(args.file)


if __name__ == "__main__":
    demo()
