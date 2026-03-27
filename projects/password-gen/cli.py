#!/usr/bin/env python3
"""
Password Generator - Generate secure passwords
"""

import argparse
import secrets
import string

def generate(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    """Generate a secure password."""
    chars = ""
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation
    
    if not chars:
        chars = string.ascii_letters + string.digits
    
    return ''.join(secrets.choice(chars) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(description="Password Generator")
    parser.add_argument("-l", "--length", type=int, default=16, help="Password length")
    parser.add_argument("--no-upper", action="store_true", help="No uppercase")
    parser.add_argument("--no-lower", action="store_true", help="No lowercase")
    parser.add_argument("--no-digits", action="store_true", help="No digits")
    parser.add_argument("--no-special", action="store_true", help="No special characters")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of passwords")
    
    args = parser.parse_args()
    
    for _ in range(args.count):
        pwd = generate(
            args.length,
            not args.no_upper,
            not args.no_lower,
            not args.no_digits,
            not args.no_special
        )
        print(pwd)

if __name__ == "__main__":
    main()