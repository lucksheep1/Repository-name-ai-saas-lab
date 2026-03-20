"""
Memory argparse_example16
argparse_example16
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", type=int)
    print(parser.parse_args(["-x", "5"]).x)


if __name__ == "__main__":
    demo()
