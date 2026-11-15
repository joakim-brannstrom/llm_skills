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
  plan documents are ephemeral. Also strips temporal/change-log comments
  ("no longer", "used to", "is gone") and design-doc citations (section
  references like §N.N, decision tags like D-ESC, requirement IDs like
  FR-09). Use when asked to review, clean, fix,
  improve, or refactor comments in any source code, or to remove dangling
  plan-artifact references. Triggers on: fix comments, clean comments,
  remove comments, comment cleanup, comment quality, redundant comments,
  outdated comments, plan artifact references, requirement ID cleanup, strip
  task references, remove gate references, line reference cleanup, temporal
  comments, change-log comments, design section references, decision tags.
version: 1.6.4
---

# Fix Comments Skill

Comments should explain **why** and **what's non-obvious**, not **what** the code
literally does. If the code is self-documenting, the comment is redundant.

## When to Use

Use this skill when the user asks to:
- Remove, clean up, condense, or fix comments in source code
- Review comment quality; fix outdated comments that no longer match the code
- Strip references to plan/requirement artifacts from comments, test strings, or docs

## Scope
## Scope

**In scope** (judged by the decision rules):
- All comment forms, including ddoc, which is **not protected** (`references/ddoc.md`).
- Comments inside unittests.
- Descriptive string literals: UDA description strings `@("...")` on
  unittests, and strings used inside unittests (assert messages, expected
  outputs) - they commonly carry plan-artifact references
  (`references/plan-artifacts.md`).
- Markdown docs (design docs, AGENTS.md, docstrings) and anchor links.

**Out of scope**: identifiers, non-descriptive string literals - left in
place, listed in the report, never skipped silently.

A string rewrite inside a unittest may require a minimal test rewrite
(reworded assert, shortened description): same assertions, same expected
values, same coverage.

**Plan references are never kept.** Plan/requirement documents are ephemeral,
so every in-scope reference is removed or rephrased.

## Classification

Classify each comment as KEEP, REMOVE, REWRITE, or UNSURE.
See `references/decision-rules.md` for concrete patterns and style rules.

## Workflow

See `references/workflow.md` for detailed steps. The run is a checkpointed
per-file loop - only on-disk state (todo, edited files, report) survives
compression.

1. **Discovery** - List target files, write the todo list to disk. Do not read file contents.
2. **Per-file loop** - Read one file, classify tersely, edit (verified after every edit), verify, mark DONE in the todo, append the report section to disk, drop the file.
3. **Report** - Present the on-disk report, clean up scratch files.

## Special Cases

- **Unit tests**: keep test purpose descriptions and limitation notes;
  plan-ref removals may need a minimal rewrite that preserves behavior.
- **Outdated comments**: update to match code, don't just remove.
- **D code (ddoc)**: in scope like regular comments. `Example:`/`Examples:`
  are compiled and run as tests - a change must not alter what they verify;
  report every touched section. `Copyright:`/`License:`/`Authors:` kept.
  See `references/ddoc.md`.
- **Plan-artifact references**: removal is rephrasing, not deletion;
  in-scope references are never kept (ephemeral documents). Design-doc
  citations are plan artifacts too: section refs, decision tags,
  requirement IDs. See `references/plan-artifacts.md`.
- **Temporal / change-log comments**: comments narrating the change
  ("now", "no longer", "is gone", "used to") describe history, not
  behavior - rewrite to present tense. See `references/decision-rules.md`.
- **Diff-scoped passes**: the scope is the lines added vs a base commit, not
  the whole file - base (context) lines keep their existing style, plan refs
  included. Added comment blocks longer than 5 lines are compressed to at
  most 5. Prose stays ASCII; glyphs that quote real UI output in mocks and
  check strings stay. See `references/decision-rules.md`.

## Anti-Patterns

- **Over-removal**: good comments add signal - don't strip all comments.
- **Bulk reads**: process one file at a time; only on-disk state survives compression.
- **Line-number drift**: track line shifts after each removal.
- **Ignoring context**: a comment may seem redundant in isolation but add value when skimming.
- **Treating ddoc as untouchable**: docs-generation is not a keep-reason.
- **Silent test changes**: confirm unittest rewrites change nothing and report them.
- **Aggressive test cleanup**: test comments explain intent assertions alone don't show.
- **Skipping verification on comment-only edits**: ddoc `Example:` sections
  and unittest strings compile, and vocabulary/golden gates read them -
  a comment-only change still requires a rebuild plus the full test run.

## References

- Decision rules and style guidelines: `references/decision-rules.md`
- Detailed workflow: `references/workflow.md`
- Ddoc handling for D code: `references/ddoc.md`
- Plan-artifact reference removal: `references/plan-artifacts.md`
- Utility scripts: `scripts/README.md`
