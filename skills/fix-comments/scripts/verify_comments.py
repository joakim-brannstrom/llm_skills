#!/usr/bin/env python3
"""
Verify comment fixes in source files.
Checks for remaining issues after comment cleanup operations.

Usage:
    python3 verify_comments.py <file> [--check-escaped] [--check-duplicates] [--check-empty]
    python3 verify_comments.py <file> --start N --end N

Examples:
    # Verify all comment issues
    python3 verify_comments.py imgui_markdown.h

    # Check specific line range
    python3 verify_comments.py imgui_markdown.h --start 930 --end 960

    # Check only for escaped slashes
    python3 verify_comments.py imgui_markdown.h --check-escaped

    # Check for empty comment lines
    python3 verify_comments.py imgui_markdown.h --check-empty
"""
import sys
import os
import re
import argparse


def check_escaped_slashes(content, start=None, end=None):
    """Check for escaped comment slashes."""
    issues = []
    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        if start and i < start:
            continue
        if end and i > end:
            break

        # Check for escaped slashes
        if r'\/' in line or r'\*' in line or r'\*' in line:
            issues.append((i, f"Escaped slash: {line.strip()[:60]}"))

    return issues


def check_duplicate_lines(content, start=None, end=None):
    """Check for duplicate consecutive lines."""
    issues = []
    lines = content.split("\n")

    for i in range(1, len(lines)):
        line_num = i + 1
        if start and line_num < start:
            continue
        if end and line_num > end:
            break

        if lines[i] == lines[i - 1]:
            issues.append((line_num, f"Duplicate line: {lines[i].strip()[:60]}"))

    return issues


def check_empty_comments(content, start=None, end=None):
    """Check for empty or near-empty comment lines."""
    issues = []
    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        if start and i < start:
            continue
        if end and i > end:
            break

        stripped = line.strip()
        # Check for empty comments
        if stripped in ("//", "/*", "*/", "*", "///"):
            issues.append((i, f"Empty comment: {stripped}"))

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Verify comment fixes in source files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Checks for:
  - Escaped comment slashes
  - Duplicate consecutive lines
  - Empty comment lines

Examples:
  %(prog)s file.h
  %(prog)s file.h --start 930 --end 960
  %(prog)s file.h --check-escaped
  %(prog)s file.h --check-empty
"""
    )
    parser.add_argument("file", help="Source file to verify")
    parser.add_argument("--start", type=int, help="Start line number")
    parser.add_argument("--end", type=int, help="End line number")
    parser.add_argument("--check-escaped", action="store_true", help="Check for escaped slashes")
    parser.add_argument("--check-duplicates", action="store_true", help="Check for duplicate lines")
    parser.add_argument("--check-empty", action="store_true", help="Check for empty comments")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"ERROR: {args.file} not found")
        sys.exit(1)

    with open(args.file) as f:
        content = f.read()

    check_all = not (args.check_escaped or args.check_duplicates or args.check_empty)

    all_issues = []

    if check_all or args.check_escaped:
        issues = check_escaped_slashes(content, args.start, args.end)
        if issues:
            all_issues.extend(("ESCAPED",) + issue for issue in issues)

    if check_all or args.check_duplicates:
        issues = check_duplicate_lines(content, args.start, args.end)
        if issues:
            all_issues.extend(("DUPLICATE",) + issue for issue in issues)

    if check_all or args.check_empty:
        issues = check_empty_comments(content, args.start, args.end)
        if issues:
            all_issues.extend(("EMPTY",) + issue for issue in issues)

    if all_issues:
        print(f"VERIFICATION ISSUES ({len(all_issues)}):")
        for issue_type, line_num, msg in all_issues:
            print(f"  [{issue_type}] Line {line_num}: {msg}")
        sys.exit(1)
    else:
        print("OK: No comment issues detected")
        sys.exit(0)


if __name__ == "__main__":
    main()
