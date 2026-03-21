"""
Memory argparse_example19
argparse_example19
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(["-v"])
    print(args.verbose)


if __name__ == "__main__":
    demo()
