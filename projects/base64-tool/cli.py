#!/usr/bin/env python3
"""
Base64 Encoder/Decoder
"""

import argparse
import base64

def encode(data):
    return base64.b64encode(data.encode()).decode()

def decode(data):
    return base64.b64decode(data.encode()).decode()

def main():
    parser = argparse.ArgumentParser(description="Base64 Encoder/Decoder")
    parser.add_argument("text", help="Text to encode/decode")
    parser.add_argument("-d", "--decode", action="store_true", help="Decode instead of encode")
    
    args = parser.parse_args()
    
    try:
        if args.decode:
            print(decode(args.text))
        else:
            print(encode(args.text))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()