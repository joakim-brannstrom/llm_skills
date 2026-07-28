---
name: fix-comments
description: >-
  Clean up and condense comments in source code files. Use when asked
  to review, clean, fix, improve, or refactor comments in any source code.
version: 1.0.0
---

# Fix Comments

## When to Use

Use this skill when the user asks to:
- Remove or clean up comments in source code
- Make comments more concise or shorter
- Fix outdated comments that no longer match the code
- Review comment quality

## Rules

**Remove comments that are:**
- **Self-explanatory from the code**: The code already says what the comment says
- **Fluff/boilerplate**: Generic statements like "Initialize variables", "Return result"
- **Obvious control flow**: "Check if X is true", "Loop through items"

**Keep comments that describe:**
- Non-obvious patterns or idioms
- Magic constants and their meanings
- Hard-to-follow control or data flows
- Design decisions and rationale
- Edge cases and caveats

**Rewrite verbose comments to be concise.** Less is more.

## Workflow

1. **Read the file** — examine every comment
2. **Classify each comment** as remove, keep, or rewrite
3. **Apply changes** — prefer `writeFile` for full rewrites to avoid incremental edit corruption
4. **Verify** — read the result, ensure no code was accidentally removed
5. **Report** — summarize what was changed in a table format

## Edge Cases

- Comments the user might want to keep: flag them as "borderline" in the report with reasoning
- Outdated comments (no longer match implementation): update them, don't just remove
- Multi-line doc comments: condense to 1-2 lines when possible
