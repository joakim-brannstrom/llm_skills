# Fix Comments Skill - Utility Scripts

Consolidated utility scripts for comment cleanup and verification tasks.

## Scripts

### `fix_comments_escaping.py`
Fix comment escaping issues in source files. Handles escaped comment slashes, redundant comment markers, and malformed comments.

```bash
# Fix escaped comment slashes (e.g., \\/\\/ -> //)
python3 fix_comments_escaping.py imgui_markdown.h --fix-escaped

# Remove duplicate consecutive lines
python3 fix_comments_escaping.py imgui_markdown.h --fix-duplicates

# Check for issues without fixing
python3 fix_comments_escaping.py imgui_markdown.h --check

# Dry run
python3 fix_comments_escaping.py imgui_markdown.h --fix-escaped --dry-run
```

**Common issues fixed:**
- Escaped comment slashes (`\/\/` -> `//`)
- Escaped block comment markers (`\/\*` -> `/*`, `\*\/` -> `*/`)
- Duplicate consecutive lines

### `check_raw_bytes.py`
Check raw bytes in source files for escaped characters. Useful for verifying comment escaping and string literal issues.

```bash
# Check specific line
python3 check_raw_bytes.py imgui_markdown.h --line 940

# Check line range
python3 check_raw_bytes.py imgui_markdown.h --start 930 --end 960

# Search for specific byte pattern (hex)
python3 check_raw_bytes.py imgui_markdown.h --pattern 5c2f

# Show all lines with backslashes
python3 check_raw_bytes.py imgui_markdown.h --pattern 5c
```

**Common patterns (hex):**
- `5c2f` = `\/` (escaped slash)
- `5c2a` = `\*` (escaped asterisk)
- `5c5c` = `\\` (escaped backslash)
- `5c` = `\` (any backslash)

### `verify_comments.py`
Verify comment fixes in source files. Checks for remaining issues after comment cleanup operations.

```bash
# Verify all comment issues
python3 verify_comments.py imgui_markdown.h

# Check specific line range
python3 verify_comments.py imgui_markdown.h --start 930 --end 960

# Check only for escaped slashes
python3 verify_comments.py imgui_markdown.h --check-escaped

# Check for empty comment lines
python3 verify_comments.py imgui_markdown.h --check-empty
```

**Checks for:**
- Escaped comment slashes
- Duplicate consecutive lines
- Empty comment lines

## Origin

These scripts were consolidated from ~20 one-off utility scripts that accumulated
in the workarea during development sessions on `imgui_markdown.h`. The original
scripts were created to fix indentation, braces, comments, and duplicate lines
in this third-party vendor file.
