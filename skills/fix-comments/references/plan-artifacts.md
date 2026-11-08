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
| Decision tags | `D-ESC`, `D-PASTE`, `D-THEME`, `D-METRICS`, `D-STATUS`, `D-KEYGATE's fallback` |
| Design-section citations | `design §4.6`, `(§4.7)`, `§4.6's degradation`, `plan/key_gate.md §4i` |
| Requirement IDs | `FR-09`, `FR-29`, `NFR-16` |
| Task attributions | `Task 28's note:`, `(task 45)`, `task 39's rule` |
| Review artifacts | `(review finding: ...)`, `the review's I1` |
| Doc version tags | `D-STATUS v5`, `the v5 contract` - a document revision pinned next to a decision ID is the same dangling citation |
| Plan-document names used as prose | `the key gate('s)`, `the design's own numbers` - re-ground the fact to the code ("the chip row's own numbers"), never to the ephemeral doc |

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

## Task References Are Always Removed

Any `task N` (or batch-tag) citation in a comment or descriptive string is a
plan artifact, no matter which batch it names - including references to
mechanisms another batch built (`task 39` structured status, `task 43` focus
mode). Keep the fact the citation carried; drop the citation:

- `the structured status once task 39 sends one` -> `the structured status when D sends one`
- `the now bar (views/nowbar.h, task 28)` -> `the now bar (views/nowbar.h)`
- `Unknown ordinals clamp instead of becoming a neighbour (task 39's rule).`
  -> `Unknown ordinals clamp instead of becoming a neighbour.`

Never mass-strip silently: when a sweep removes references to other batches'
mechanisms, say so in the report with the file:line count.

## Worked Rewrite Examples

Real before/after pairs from a cleanup pass (C++/D UI code, a batch that moved
the context meter from the composer to the now bar and removed the top bar's
run pill):

| Before | After |
|--------|-------|
| `see their query in (design §4.6's degradation; B4 - the block is the mode word alone now, the model name having moved to the now bar)` | `see their query in - the block is the mode word alone, and the model name lives on the now bar` |
| `the RAW badge and the settings entry (B4: the run pill is gone - the run's clock and state live on the now bar, the row that owns the run's story ...)` | `the RAW badge and the settings entry (the run's clock and state live on the now bar, the row that owns the run's story ...)` |
| `The context meter's segment counts - the meter's own vocabulary, kept here after B4 moved the meter itself to the now bar (...)` | `The context meter's segment counts - the meter's own vocabulary, shared by both bars so they read the same thresholds and can never disagree (...)` |
| `The meter's segment count on the pixel profile (B4): fewer than the composer's ten` | `The meter's segment count on the pixel profile: fewer than the shared kMeterSegmentsGui ten` |
| `the composer's meter used to (StatusChips::contextUsed/contextMax)` | `the count beside it is drawn from (StatusChips::contextUsed/contextMax)` |
| `seven phases (design §4.7)` (assert message) | `seven phases` |
| `The coarse Ready/Busy chip is gone with the rest of the four-chip strip - the idle row's phase word *is* ready, and the sentence's state word survives in the thread and the log where it belongs (B4).` | `The coarse Ready/Busy word lives in the thread and the log, where it belongs - the idle row's phase word *is* ready.` |

Pattern in all of them: the citation or history clause is deleted; any fact it
carried that the sentence still needs (who owns what, which constant, which
rule) is folded into the present-tense sentence. Never leave a sentence
addressing a reader who remembers the old code.
