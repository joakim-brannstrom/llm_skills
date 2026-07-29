#!/usr/bin/env python3
"""
Check raw bytes in source files for escaped characters.
Useful for verifying comment escaping and string literal issues.

Usage:
    python3 check_raw_bytes.py <file> [--line N] [--start N] [--end N] [--pattern <hex>]

Examples:
    # Check specific line
    python3 check_raw_bytes.py imgui_markdown.h --line 940

    # Check line range
    python3 check_raw_bytes.py imgui_markdown.h --start 930 --end 960

    # Search for specific byte pattern (hex)
    python3 check_raw_bytes.py imgui_markdown.h --pattern 5c2f

    # Show all lines with backslashes
    python3 check_raw_bytes.py imgui_markdown.h --pattern 5c
"""
import sys
import os
import argparse


def hex_to_bytes(hex_str):
    """Convert hex string to bytes."""
    return bytes.fromhex(hex_str)


def check_line_raw(content, line_num, pattern=None):
    """Check raw bytes of a specific line."""
    lines = content.split("\n")
    if line_num < 1 or line_num > len(lines):
        print(f"ERROR: Line {line_num} out of range (1-{len(lines)})")
        return None

    line = lines[line_num - 1]
    line_bytes = line.encode("utf-8")

    result = {
        "line": line_num,
        "text": line,
        "bytes": line_bytes,
        "hex": line_bytes.hex(),
        "length": len(line_bytes),
    }

    if pattern:
        pattern_bytes = hex_to_bytes(pattern)
        if pattern_bytes in line_bytes:
            result["match"] = True
            result["pattern"] = pattern
        else:
            result["match"] = False

    return result


def check_range_raw(content, start, end, pattern=None):
    """Check raw bytes of a line range."""
    lines = content.split("\n")
    results = []

    for i in range(start - 1, min(end, len(lines))):
        line = lines[i]
        line_bytes = line.encode("utf-8")

        if pattern:
            pattern_bytes = hex_to_bytes(pattern)
            if pattern_bytes in line_bytes:
                results.append({
                    "line": i + 1,
                    "text": line,
                    "bytes": line_bytes,
                    "hex": line_bytes.hex(),
                    "length": len(line_bytes),
                    "match": True,
                    "pattern": pattern,
                })
        else:
            results.append({
                "line": i + 1,
                "text": line,
                "bytes": line_bytes,
                "hex": line_bytes.hex(),
                "length": len(line_bytes),
            })

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Check raw bytes in source files for escaped characters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Common patterns (hex):
  5c2f = \\/ (escaped slash)
  5c2a = \\* (escaped asterisk)
  5c5c = \\\\ (escaped backslash)
  5c = \\ (any backslash)

Examples:
  %(prog)s file.h --line 940
  %(prog)s file.h --start 930 --end 960
  %(prog)s file.h --pattern 5c2f
  %(prog)s file.h --pattern 5c
"""
    )
    parser.add_argument("file", help="Source file to check")
    parser.add_argument("--line", type=int, help="Specific line number to check")
    parser.add_argument("--start", type=int, help="Start line number")
    parser.add_argument("--end", type=int, help="End line number")
    parser.add_argument("--pattern", help="Hex pattern to search for (e.g., 5c2f)")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"ERROR: {args.file} not found")
        sys.exit(1)

    with open(args.file) as f:
        content = f.read()

    if args.line:
        result = check_line_raw(content, args.line, args.pattern)
        if result:
            print(f"Line {result['line']}:")
            print(f"  Text: {result['text'][:80]}")
            print(f"  Length: {result['length']} bytes")
            print(f"  Hex: {result['hex'][:100]}...")
            if args.pattern:
                print(f"  Pattern {args.pattern}: {'FOUND' if result.get('match') else 'NOT FOUND'}")

    elif args.start and args.end:
        results = check_range_raw(content, args.start, args.end, args.pattern)
        print(f"Lines {args.start}-{args.end}:")
        for result in results:
            if args.pattern and result.get("match"):
                print(f"  Line {result['line']}: {result['text'][:80]}")
        if not results and args.pattern:
            print(f"  No lines match pattern {args.pattern}")

    else:
        # Default: show file info
        total_lines = len(content.split("\n"))
        total_bytes = len(content.encode("utf-8"))
        print(f"File: {args.file}")
        print(f"Lines: {total_lines}")
        print(f"Bytes: {total_bytes}")
        print(f"Use --line N or --start N --end M to check specific lines")

    sys.exit(0)


if __name__ == "__main__":
    main()
