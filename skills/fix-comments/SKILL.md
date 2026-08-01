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

Classify each comment as KEEP, REMOVE, REWRITE, or UNSURE.
See `references/decision-rules.md` for concrete patterns and style rules.

## Workflow

See `references/workflow.md` for detailed steps.

1. **Discovery** — List target files, read completely, catalog all comments.
2. **Classification** — Classify each comment using decision rules.
3. **Execution** — Apply edits (single-file: `editFile`; multi-file: Python script).
4. **Verification** — Re-read modified files, confirm no code removed.
5. **Report** — Summarize changes in table format with reasons.

## Special Cases

- **Unit tests**: Keep test purpose descriptions and limitation notes.
- **Outdated comments**: Update to match code, don't just remove.
- **Doc tool blocks** (`/** */`, `///`): Don't remove unless explicitly asked.
- **D code (ddoc)**: Ddoc comments feed the documentation generator. See `references/ddoc.md`.

## Anti-Patterns

- **Over-removal**: Good comments add signal — don't strip all comments.
- **Line-number drift**: Track line shifts after each removal.
- **Ignoring context**: A comment may seem redundant in isolation but add value when skimming.
- **Breaking doc tools**: Preserve blocks feeding documentation generators.
- **Aggressive test cleanup**: Test comments explain intent assertions alone don't show.

## References

- Decision rules and style guidelines: `references/decision-rules.md`
- Detailed workflow: `references/workflow.md`
- Ddoc handling for D code: `references/ddoc.md`
- Utility scripts: `scripts/README.md`
