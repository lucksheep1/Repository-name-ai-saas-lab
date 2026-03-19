"""
Memory argparse_example4
argparse_example4
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args(["--count", "5"])
    print(args.count)


if __name__ == "__main__":
    demo()
