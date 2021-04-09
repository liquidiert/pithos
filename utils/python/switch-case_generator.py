#!/usr/bin/python3

"""
A simple switch-case generator for long switches. Use with regex like ranges; e.g. a-z, a-Z
"""

import sys

if __name__=="__main__":
    args = sys.argv[1:]
    start, end = args[0].split("-")
    start, end = ord(start), ord(end)
    if start > end:
        start, end = end, start

    print("switch (replace_me) {")
    for i in range(start, end+1):
        if i >= 91 and i <= 96:
            continue
        print(f"  case '{chr(i)}':")
        print("    break;")
    print("  default:")
    print("    // do handling here")
    print("    break;")
    print("}")
