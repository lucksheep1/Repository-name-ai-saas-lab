"""
Memory argparse_example9
argparse_example9
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=10)
    args = parser.parse_args(["-n", "5"])
    print(args.n)


if __name__ == "__main__":
    demo()
