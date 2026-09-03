# Plan-Artifact References — Removal Guide

Use when the task is to strip references to a plan/requirements artifact
(tasks, phases, requirement IDs, gates) from comments and docs — i.e. the
referenced planning document was deleted or is out of scope, and the
references now dangle.

## Prerequisites

- **Verify the referent is actually gone.** If the ID system is still live in a
  living document, the IDs are traceability, not noise — keep them.
- **Scope the file set explicitly.** "Files changed since commit X" =
  `git diff --name-only X..HEAD`. Do not widen to the whole repo on your own.
- **Separate product features from plan artifacts.** A `/plan` slash command
  documented in a README is a product feature — keep it. A "P3 Task 6"
  comment is a plan artifact — remove it.

## What Counts as a Plan Artifact

| Kind | Examples |
|------|----------|
| Task references | `Task 6`, `plan Task 3`, `P3 (Task 6) second run` |
| Phase references | `Phase 2`, `Phase 4`, `until Phase 3`, `P3 DP scoring` |
| Requirement/decision IDs | `(A28)`, `(R6/A6/H1)`, `**A28 — ...**`, `D12 regex` |
| Gate names | `byte-stream gate`, `overall gate status` |
| Cross-document section refs | `design §7 Task 3`, `see requirements R25` |

## Scope: Comments, Not Code (default)

The same strings often appear in string literals, printed output, and
identifiers (`r2_cap`, `print("R2 max-width gate FAILED: ...")`). Default
scope is comments and doc prose only. When code references are left
in place, list them explicitly in the report as intentionally untouched —
never silently skip them.

## How to Remove — Rephrase, Don't Just Delete

| Position | Before | After |
|----------|--------|-------|
| Trailing parenthetical | `(no overlap, R6/A6/H1)` | `(no overlap)` |
| Trailing mid-sentence | `never per frame (L3); a title` | `never per frame; a title` |
| Leading bold label | `**A28 — rename box closes when its row is filtered out**:` | `**Rename box closes when its row is filtered out**:` |
| Cross-reference | `and A28 (below) guarantees` | `and the rule below guarantees` |
| Plan-phase adjective | `for the P3 DP scoring` | `for future DP scoring` |
| Heading suffix | `### Filter Input (Phase 4)` | `### Filter Input` |
| "Until phase" clause | `unreachable until Phase 3` | `unreachable` |

Punctuation must survive: no dangling commas, doubled spaces, or orphaned
em dashes. Re-read the full sentence after every removal.

## Docs and Anchor Links

Markdown docs are in scope (design docs, AGENTS.md bullets, docstrings).
Renaming a heading changes its GitHub-style anchor — update every internal
link in the same pass:
`[Filter Input (Phase 4)](#filter-input-phase-4)` → `[Filter Input](#filter-input)`.
After renaming, grep the repo for the old anchor text to catch stragglers.

## Discovery

Pattern-grep the target set instead of skimming — IDs hide in code-block
comments and doc prose:

```
grep -n -E 'Phase [0-9]|Task [0-9]|P[0-9] |gate|\b[AFHNLST][0-9]+\b' <files>
```

Letter+digit patterns produce false positives ("wipe" ~ "wip", "UTF-8",
`TUI_API_VERSION`) — eyeball every hit before editing.

## Report Additions

On top of the standard report, include:
- **Left in place (code, out of comment scope)**: file:line — identifier/string
- **Left in place (product feature)**: file:line — why it is not an artifact
- **Anchor links updated**: old → new
