---
name: fix-comments
description: >-
  Clean up and condense comments in source code. Scope covers all comment
  forms — ddoc (`/** */`, `///`, `/++ ...`) is not protected — plus comments
  and descriptive strings in unittests (UDA description strings, assert
  messages). Remove redundant, obvious, and outdated comments while keeping
  those that explain non-obvious behavior. Also strips references to
  plan/requirement artifacts (task IDs, phases, decision points, gates) from
  comments, test strings, and docs; plan references are never kept because
  plan documents are ephemeral. Use when asked to review, clean, fix,
  improve, or refactor comments in any source code, or to remove dangling
  plan-artifact references. Triggers on: fix comments, clean comments,
  remove comments, comment cleanup, comment quality, redundant comments,
  outdated comments, plan artifact references, requirement ID cleanup, strip
  task references, remove gate references, line reference cleanup.
version: 1.3.0
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
- Strip references to plan/requirement artifacts (tasks, phases, decision points, gates) from comments, test strings, or docs

## Scope

**In scope** (judged by the decision rules):
- All comment forms — including ddoc (`/** */`, `/++ ... +/`, `///`), which
  is **not protected** (`references/ddoc.md`).
- Comments inside unittests.
- Descriptive string literals: UDA description strings `@("...")` on
  unittests, and strings used inside unittests (assert messages, expected
  outputs) — they commonly carry plan-artifact references
  (`references/plan-artifacts.md`).
- Markdown docs (design docs, AGENTS.md, docstrings) and anchor links.

**Out of scope**: identifiers, non-descriptive string literals — left in
place, listed in the report, never skipped silently.

A string rewrite inside a unittest may require a minimal test rewrite
(reworded assert, shortened description): same assertions, same expected
values, same coverage.

**Plan references are never kept.** Plan/requirement documents are ephemeral
— deleted after the work — so every in-scope reference is removed or rephrased.

## Classification

Classify each comment as KEEP, REMOVE, REWRITE, or UNSURE.
See `references/decision-rules.md` for concrete patterns and style rules.

## Workflow

See `references/workflow.md` for detailed steps. The run is a checkpointed
per-file loop — only on-disk state (todo, edited files, report) survives
compression.

1. **Discovery** — List target files, write the todo list to disk. Do not read file contents.
2. **Per-file loop** — For each file: read it (one at a time), classify tersely, edit (few edits: `editFile`; many: one atomic `applyDiff`), verify, mark DONE in the todo list, append the per-file report section to disk, drop the file.
3. **Report** — Present the accumulated on-disk report, clean up scratch files.

## Special Cases

- **Unit tests**: Keep test purpose descriptions and limitation notes.
  Comments and strings in unittests are in scope; plan-ref removals may
  need a minimal test rewrite that preserves behavior.
- **Outdated comments**: Update to match code, don't just remove.
- **D code (ddoc)**: In scope like regular comments. `Example:`/`Examples:`
  are compiled and run as tests — a change must not alter what they verify;
  report every touched section. `Copyright:`/`License:`/`Authors:` kept.
  See `references/ddoc.md`.
- **Plan-artifact references**: removal is rephrasing, not deletion;
  in-scope references are never kept (ephemeral documents). See
  `references/plan-artifacts.md`.

## Anti-Patterns

- **Over-removal**: Good comments add signal — don't strip all comments.
- **Bulk reads**: Loading multiple target files into context at once — process one file at a time; only durable on-disk state survives compression.
- **Line-number drift**: Track line shifts after each removal.
- **Ignoring context**: A comment may seem redundant in isolation but add value when skimming.
- **Treating ddoc as untouchable**: docs-generation is not a keep-reason.
- **Silent test changes**: confirm unittest rewrites change nothing and report them — coverage must never change invisibly.
- **Aggressive test cleanup**: Test comments explain intent assertions alone don't show.

## References

- Decision rules and style guidelines: `references/decision-rules.md`
- Detailed workflow: `references/workflow.md`
- Ddoc handling for D code: `references/ddoc.md`
- Plan-artifact reference removal: `references/plan-artifacts.md`
- Utility scripts: `scripts/README.md`
