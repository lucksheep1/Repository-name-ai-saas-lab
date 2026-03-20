"""
Memory argparse_example17
argparse_example17
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count")
    args = parser.parse_args(["-vvv"])
    print(args.verbose)


if __name__ == "__main__":
    demo()
