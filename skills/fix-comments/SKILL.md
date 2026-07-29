---
name: fix-comments
description: >-
  Clean up and condense comments in source code. Remove redundant, obvious, and
  outdated comments while keeping those that explain non-obvious behavior. Use
  when asked to review, clean, fix, improve, or refactor comments in any source
  code. Triggers on: fix comments, clean comments, remove comments, comment
  cleanup, comment quality, redundant comments, outdated comments.
version: 1.0.0
---

# Fix Comments Skill

Audit and clean up source code comments. Eliminate redundancy, fix inaccuracies,
and enforce a "code-first" documentation philosophy.

## Core Principle

Comments should explain **why** and **what's non-obvious**, not **what** the code
literally does. If the code is self-documenting, the comment is redundant.

## When to Use

Use this skill when the user asks to:
- Remove or clean up comments in source code
- Make comments more concise or shorter
- Fix outdated comments that no longer match the code
- Review comment quality

## Classification

Classify each comment into one of four categories:

| Category | Action | Criteria |
|----------|--------|----------|
| **KEEP** | Leave as-is | Explains non-obvious behavior, architecture, edge cases, external APIs, thread-safety, lifecycle, field relationships, module docs, license info |
| **REMOVE** | Delete | Restates what code shows, obvious control flow, task references, section markers, wrong/outdated content |
| **REWRITE** | Condense | Verbose but contains useful information — trim to 1-2 lines |
| **UNSURE** | Keep and flag | Uncertain — note location, text, and reasoning in report |

See `references/decision-rules.md` for concrete patterns with examples.

## Workflow

Follow the protocol. See `references/workflow.md` for detailed steps.

1. **Discovery** — List target files, read completely, catalog all comments with line numbers and types.
2. **Classification** — Classify each comment as KEEP, REMOVE, REWRITE, or UNSURE.
3. **Execution** — Apply edits (single-file: `editFile`; multi-file: Python script for bulk).
4. **Verification** — Re-read modified files, confirm no code removed, check formatting.
5. **Report** — Summarize changes in table format with reasons.

## Special Cases

- **Unit tests**: Keep test purpose descriptions, limitation notes, and integration instructions.
- **Outdated comments**: Update to match code, don't just remove.
- **Multi-line doc comments**: Condense to 1-2 lines when possible.
- **Doc tool blocks** (`/** */`, `///`): Don't remove unless explicitly asked.
- **D code (ddoc)**: Ddoc comments (`/** */`, `///`, `/+ +/`) feed the documentation generator. See `references/ddoc.md`.

## Anti-Patterns

- **Over-removal**: Good comments add signal — don't strip all comments.
- **Line-number drift**: Track line shifts after each removal.
- **Ignoring context**: A comment may seem redundant in isolation but add value when skimming.
- **Breaking doc tools**: Preserve blocks feeding documentation generators.
- **Aggressive test cleanup**: Test comments explain intent assertions alone don't show.

## References

- Decision rules with examples: `references/decision-rules.md`
- Detailed workflow: `references/workflow.md`
- Ddoc handling for D code: `references/ddoc.md`
- Utility scripts: `scripts/README.md`

## Utility Scripts

See `scripts\/README.md` for full documentation. Quick reference:

| Script | Purpose |
|--------|---------|
| `fix_comments_escaping.py` | Fix escaped comment slashes, duplicates |
| `check_raw_bytes.py` | Check raw bytes for escaped characters |
| `verify_comments.py` | Verify comment fixes, check remaining issues |

- Ddoc handling for D code: `references/ddoc.md`
