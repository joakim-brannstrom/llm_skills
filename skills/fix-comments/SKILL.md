---
name: fix-comments
description: >-
  Clean up and condense comments in source code. Remove redundant, obvious, and
  outdated comments while keeping those that explain non-obvious behavior. Also
  strips references to plan/requirement artifacts (task IDs, phases,
  requirement IDs, gates) from comments and docs. Use when asked to review,
  clean, fix, improve, or refactor comments in any source code, or to remove
  dangling plan-artifact references. Triggers on: fix comments, clean comments,
  remove comments, comment cleanup, comment quality, redundant comments,
  outdated comments, plan artifact references, requirement ID cleanup, strip
  task references, remove gate references.
version: 1.1.0
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
- Strip references to plan/requirement artifacts (tasks, phases, requirement IDs, gates) from comments or docs

## Classification

Classify each comment as KEEP, REMOVE, REWRITE, or UNSURE.
See `references/decision-rules.md` for concrete patterns and style rules.

## Workflow

See `references/workflow.md` for detailed steps. The run is a checkpointed
per-file loop — only on-disk state (todo list, edited files, report)
reliably survives context compression.

1. **Discovery** — List target files, write the todo list to disk. Do not read file contents.
2. **Per-file loop** — For each file: read it (one at a time), classify tersely, edit (few edits: `editFile`; many: one atomic `applyDiff`), verify, mark DONE in the todo list, append the per-file report section to disk, drop the file.
3. **Report** — Present the accumulated on-disk report, clean up scratch files.

## Special Cases

- **Unit tests**: Keep test purpose descriptions and limitation notes.
- **Outdated comments**: Update to match code, don't just remove.
- **Doc tool blocks** (`/** */`, `///`): Don't remove unless explicitly asked.
- **D code (ddoc)**: Ddoc comments feed the documentation generator. See `references/ddoc.md`.
- **Plan-artifact references**: removal is rephrasing, not deletion; docs and anchor links are in scope; code identifiers/strings are out of scope by default. See `references/plan-artifacts.md`.

## Anti-Patterns

- **Over-removal**: Good comments add signal — don't strip all comments.
- **Bulk reads**: Loading multiple target files into context at once — process one file at a time; only durable on-disk state survives compression.
- **Line-number drift**: Track line shifts after each removal.
- **Ignoring context**: A comment may seem redundant in isolation but add value when skimming.
- **Breaking doc tools**: Preserve blocks feeding documentation generators.
- **Aggressive test cleanup**: Test comments explain intent assertions alone don't show.

## References

- Decision rules and style guidelines: `references/decision-rules.md`
- Detailed workflow: `references/workflow.md`
- Ddoc handling for D code: `references/ddoc.md`
- Plan-artifact reference removal: `references/plan-artifacts.md`
- Utility scripts: `scripts/README.md`
