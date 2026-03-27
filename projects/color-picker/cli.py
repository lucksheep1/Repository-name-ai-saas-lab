#!/usr/bin/env python3
"""
Color Picker - Generate color codes
"""

import argparse
import random

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"#{r:02x}{g:02x}{b:02x}", f"rgb({r},{g},{b})"

def main():
    parser = argparse.ArgumentParser(description="Color Picker")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of colors")
    parser.add_argument("-s", "--scheme", choices=["random", "pastel", "dark", "bright"], default="random")
    
    args = parser.parse_args()
    
    for _ in range(args.count):
        if args.scheme == "random":
            hex, rgb = random_color()
        elif args.scheme == "pastel":
            r = random.randint(200, 255)
            g = random.randint(200, 255)
            b = random.randint(200, 255)
            hex, rgb = f"#{r:02x}{g:02x}{b:02x}", f"rgb({r},{g},{b})"
        elif args.scheme == "dark":
            r = random.randint(0, 100)
            g = random.randint(0, 100)
            b = random.randint(0, 100)
            hex, rgb = f"#{r:02x}{g:02x}{b:02x}", f"rgb({r},{g},{b})"
        else:  # bright
            r = random.randint(150, 255)
            g = random.randint(150, 255)
            b = random.randint(150, 255)
            hex, rgb = f"#{r:02x}{g:02x}{b:02x}", f"rgb({r},{g},{b})"
        
        print(f"HEX: {hex}  {rgb}")

if __name__ == "__main__":
    main()