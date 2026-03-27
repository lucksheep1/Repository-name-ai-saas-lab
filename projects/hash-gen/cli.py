#!/usr/bin/env python3
"""
Hash Generator - Generate various hashes
"""

import argparse
import hashlib
import base64

def md5(s): return hashlib.md5(s.encode()).hexdigest()
def sha1(s): return hashlib.sha1(s.encode()).hexdigest()
def sha256(s): return hashlib.sha256(s.encode()).hexdigest()
def sha512(s): return hashlib.sha512(s.encode()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Hash Generator")
    parser.add_argument("text", help="Text to hash")
    parser.add_argument("-a", "--algo", default="sha256", choices=["md5", "sha1", "sha256", "sha512"])
    
    args = parser.parse_args()
    
    func = {"md5": md5, "sha1": sha1, "sha256": sha256, "sha512": sha512}[args.algo]
    print(func(args.text))

if __name__ == "__main__":
    main()