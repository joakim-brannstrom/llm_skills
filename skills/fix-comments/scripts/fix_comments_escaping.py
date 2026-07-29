#!/usr/bin/env python3
"""
Fix comment escaping issues in source files.
Handles escaped comment slashes, redundant comment markers, and malformed comments.

Usage:
    python3 fix_comments_escaping.py <file> [--fix-escaped] [--fix-duplicates] [--dry-run]
    python3 fix_comments_escaping.py <file> --check

Examples:
    # Fix escaped comment slashes (e.g., \\/\\/ -> //)
    python3 fix_comments_escaping.py imgui_markdown.h --fix-escaped

    # Remove duplicate consecutive lines
    python3 fix_comments_escaping.py imgui_markdown.h --fix-duplicates

    # Check for issues without fixing
    python3 fix_comments_escaping.py imgui_markdown.h --check

    # Dry run to see what would change
    python3 fix_comments_escaping.py imgui_markdown.h --fix-escaped --dry-run
"""
import sys
import os
import re
import argparse


def fix_escaped_comments(content):
    """
    Fix escaped comment slashes in source files.

    Common issues:
    - \\/\\/ -> // (escaped comment start)
    - \\/\\* -> /* (escaped block comment start)
    - \\*\\/ -> */ (escaped block comment end)
    """
    fixes = 0
    original = content

    # Fix escaped single-line comment starts
    # Pattern: backslash followed by / followed by /
    content = re.sub(r'\\\\\\/\\/\\/\\/\\/', '//', content)  # Fix quadruple-escaped
    content = re.sub(r'\\\\\\/\\/', '//', content)  # Fix double-escaped

    # Fix escaped block comment starts
    content = re.sub(r'\\\\\\/\\*\\*\\*', '/*', content)
    content = re.sub(r'\\\\\\/\\*', '/*', content)

    # Fix escaped block comment ends
    content = re.sub(r'\\\\\\*\\*\\/\\/\\/', '*/', content)
    content = re.sub(r'\\\\\\*\\/\\/', '*/', content)

    fixes = 1 if content != original else 0
    return content, fixes


def remove_duplicate_lines(content):
    """Remove consecutive duplicate lines."""
    lines = content.split("\n")
    new_lines = []
    duplicates_removed = 0

    for line in lines:
        if new_lines and line == new_lines[-1]:
            duplicates_removed += 1
        else:
            new_lines.append(line)

    return "\n".join(new_lines), duplicates_removed


def check_comment_issues(content):
    """Check for common comment issues."""
    issues = []
    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        # Check for escaped comment slashes
        if r'\/\/' in line or r'\/\*' in line or r'\*\/' in line:
            issues.append((i, f"Escaped comment slash: {line.strip()[:60]}"))

        # Check for duplicate consecutive lines
        if i > 1 and line == lines[i - 2]:
            issues.append((i, f"Duplicate line: {line.strip()[:60]}"))

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Fix comment escaping issues in source files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Common issues fixed:
  - Escaped comment slashes (\\/\\/ -> //)
  - Duplicate consecutive lines
  - Malformed comment markers

Examples:
  %(prog)s file.h --fix-escaped
  %(prog)s file.h --fix-duplicates
  %(prog)s file.h --check
  %(prog)s file.h --fix-escaped --dry-run
"""
    )
    parser.add_argument("file", help="Source file to fix")
    parser.add_argument("--fix-escaped", action="store_true", help="Fix escaped comment slashes")
    parser.add_argument("--fix-duplicates", action="store_true", help="Remove duplicate consecutive lines")
    parser.add_argument("--check", action="store_true", help="Only check for issues")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"ERROR: {args.file} not found")
        sys.exit(1)

    with open(args.file) as f:
        content = f.read()

    if args.check:
        issues = check_comment_issues(content)
        if issues:
            print(f"COMMENT ISSUES ({len(issues)}):")
            for line_num, msg in issues:
                print(f"  Line {line_num}: {msg}")
            sys.exit(1)
        else:
            print("OK: No comment issues detected")
            sys.exit(0)

    original = content
    total_fixes = 0

    if args.fix_escaped:
        content, fixes = fix_escaped_comments(content)
        if fixes:
            print("Fixed escaped comment slashes")
            total_fixes += fixes

    if args.fix_duplicates:
        content, duplicates = remove_duplicate_lines(content)
        if duplicates:
            print(f"Removed {duplicates} duplicate lines")
            total_fixes += duplicates

    if content != original:
        if args.dry_run:
            print("\nDRY RUN - changes not written")
            print(f"File would change from {len(original)} to {len(content)} bytes")
        else:
            with open(args.file, "w") as f:
                f.write(content)
            print(f"File updated: {len(original)} -> {len(content)} bytes")
    else:
        print("No changes needed")

    sys.exit(0)


if __name__ == "__main__":
    main()
