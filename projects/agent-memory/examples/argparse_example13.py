"""
Memory argparse_example13
argparse_example13
"""
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-n", "--name", default="World")
    args = parser.parse_args()
    if args.verbose:
        print(f"Hello, {args.name}!")
    else:
        print(f"Hello, {args.name}")


if __name__ == "__main__":
    main()
