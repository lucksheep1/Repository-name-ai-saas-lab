#!/usr/bin/env python3
"""
Random Choice - Randomly choose from list
"""

import argparse
import random

def main():
    parser = argparse.ArgumentParser(description="Random Choice")
    parser.add_argument("items", nargs="+", help="Items to choose from")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number to choose")
    parser.add_argument("--unique", action="store_true", help="No duplicates")
    
    args = parser.parse_args()
    
    if args.unique and args.count > len(args.items):
        args.count = len(args.items)
    
    choices = random.sample(args.items, args.count) if args.unique else random.choices(args.items, k=args.count)
    for c in choices:
        print(c)

if __name__ == "__main__":
    main()