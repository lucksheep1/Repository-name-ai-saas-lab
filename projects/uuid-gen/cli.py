#!/usr/bin/env python3
"""
UUID Generator - Generate UUIDs
"""

import argparse
import uuid

def main():
    parser = argparse.ArgumentParser(description="UUID Generator")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of UUIDs")
    parser.add_argument("-u", "--upper", action="store_true", help="Uppercase")
    
    args = parser.parse_args()
    
    for _ in range(args.count):
        u = str(uuid.uuid4())
        if args.upper:
            u = u.upper()
        print(u)

if __name__ == "__main__":
    main()