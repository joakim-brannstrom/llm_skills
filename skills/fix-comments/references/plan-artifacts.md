# Plan-Artifact References — Removal Guide

Use when the task is to strip references to a plan/requirements artifact
(tasks, phases, requirement IDs, decision points, gates) from comments,
descriptive strings, and docs.

## Prerequisites

- **Plan documents are ephemeral.** They are deleted after the work is done,
  so every reference to one dangles by definition. **No in-scope reference
  may be kept** — even if the referenced document still exists today, it will
  not exist when the next reader looks at the code. There is no "keep as
  traceability" option.
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

## Scope

**In scope** — references found here MUST be removed or rephrased:
- All comments, in any comment form — including ddoc (`/** */`, `/++ ... +/`,
  `///`) and comments inside unittests.
- Descriptive string literals:
  - UDA strings describing unittests: `@("...")` on the line above `unittest {`.
  - Strings used inside unittests: assert messages, expected-output strings,
    test names. These commonly carry task/decision-point references.
- Markdown docs (design docs, AGENTS.md bullets, docstrings) and their
  anchor links.

**Out of scope** — leave in place and list them explicitly in the report
(never silently skip):
- Identifiers (`r2_cap`, `Task3Gate`) and code logic.
- Non-descriptive string literals: protocol data, log prefixes, config keys.

**Tests may be rewritten slightly.** Removing a reference from a string in a
unittest can require touching the test around it — a reworded assert message,
a shortened UDA description, a restructured string concatenation. Keep the
change minimal: same assertions, same expected values, same coverage. Never
change what a test verifies to make a reference disappear.

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
comments, doc prose, and descriptive strings (unittest UDA descriptions,
assert messages) too:

```
grep -n -E 'Phase [0-9]|Task [0-9]|P[0-9] |gate|\b[AFHNLST][0-9]+\b' <files>
```

For reference-removal jobs, also grep the string-literal lines in unittests —
UDA description strings and assert messages:

```
grep -n -E '@\("[^"]*"' <files>      # UDA strings on unittests
grep -n -E 'assert\([^)]*"[^"]*(Task|Phase|P[0-9]|\b[AFHNLST][0-9]+\b)' <files>
```

Letter+digit patterns produce false positives ("wipe" ~ "wip", "UTF-8",
`TUI_API_VERSION`) — eyeball every hit before editing.

## Report Additions

On top of the standard report, include:
- **Left in place (out of scope)**: file:line — identifier / non-descriptive string
- **Left in place (product feature)**: file:line — why it is not an artifact
- **Tests touched**: file:line — what was rewritten and confirmation that test behavior is unchanged
- **Anchor links updated**: old → new
