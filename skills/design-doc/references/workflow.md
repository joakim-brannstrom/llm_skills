# design-doc — Workflow Protocol

## Scratch layout

`scratch/<docslug>/` where `docslug` = target doc filename without extension.

| File | Step |
|------|------|
| 00-scope.md | S0 |
| 01-intent.md | S1 |
| 02a-\<group\>.md, 02b-… | S2 (one file per module group) |
| 03-flows.md | S3 |
| 04-conventions.md | S4 |
| 05-outline.md | S5 |
| 07-verification.md | S7 |

Every artifact starts with a two-line header so any step (including a
post-compression instance) can tell its state:

```
# <Step name> — <feature> (<repo> @ <short-rev>)
Status: DONE | PARTIAL
```

An artifact marked `PARTIAL` must be finished before the next step starts.
After every artifact is written, the step is safe to compact: the next step
needs only the file on disk.

## S0 — Scope

1. Confirm (or infer and state) four inputs:
   - feature to document
   - target doc path — default `<docdir>/<snake_case_feature>.md`
   - revision — default `HEAD`; if the work tree is dirty, say so: the doc
     describes the revision, and uncommitted changes must be flagged
   - constraints — default: self-contained (no plan-artifact references),
     big brush, house style of the target directory
2. Record in 00-scope.md:
   - `git rev-parse --short HEAD` and `git status --short`
   - `ls` of the target doc directory (candidate style sources)
   - one-paragraph purpose of the feature (working statement; refined in S1)
3. Stop and ask if any of the four inputs is genuinely ambiguous.

## S1 — Intent (what + why)

Sources, in authority order:
1. the plan / system-design document for this feature, if the user pointed to
   one (e.g. `plan/*.md`)
2. if none: derive intent from code, tests, and commit history
   (`git log --oneline -20 -- <feature paths>`)

Extract into 01-intent.md:
- the problem the feature solves (one paragraph)
- goals, in priority order
- non-goals / out of scope (explicit list — the doc's "Scope" section comes
  from here)
- core design rules — the one-sentence invariants the whole design hangs on
  (e.g. "only what is actually compressed gets indexed"). These become the
  spine of the doc.
- intended interactions with the rest of the system
- discrepancy flags: anywhere the plan and the code may differ. Resolve them
  in S2/S3 — the code wins.

## S2 — Implementation (how) — the big step

1. Inventory: grep the feature's key types across `source/` to enumerate its
   modules. List them all in the first 02x artifact header.
2. Work in module groups (2–4 modules, or one group per thread of
   responsibility). Per group:
   - read module headers / struct / class definitions first (the shape),
     then the key functions
   - use targeted greps for constants and thresholds instead of full-file
     reads where possible — context economy is the whole point
   - record per module: responsibility; key public types / messages /
     delegates; entry points; thread ownership; interactions with other
     modules; what is persisted and where
3. Verification rule (hard): every identifier, constant, threshold, default,
   or ordering claim must come from a grep/read this session; record the
   anchor (file:line) next to the claim in the artifact.
4. Write each group's artifact as soon as that group is analyzed. Never hold
   two groups' details in context at once — that is exactly what compression
   loses.

## S3 — Flows

Trace each path end-to-end — trigger → steps (marking thread and message
boundaries) → result. At minimum:
1. startup / wiring — registration order matters; record it exactly
2. the main event pipeline (e.g. trigger → synchronous handler → async
   worker)
3. the read / query path
4. shutdown / teardown — the order, and why that order
5. error / degradation path per stage: what happens when each stage fails
6. durability & consistency: what is durable when; invariants that stay true

Write to 03-flows.md.

## S4 — Conventions

Read 2–3 sibling docs in the target directory fully. Record in
04-conventions.md: title/intro pattern; TOC or not; sections used; table
usage; depth (what is in, what is deliberately out); naming and
cross-reference style; how failure modes and limitations are presented.

## S5 — Outline

- table of contents (sections + subsections)
- for each section: which artifact(s) supply its content (artifact + region)
- list of facts that must be re-verified before writing (every concrete
  claim: names, constants, thresholds, orderings, defaults)
- expected document length

Write to 05-outline.md.

## S6 — Write

1. Re-read 04-conventions.md; adopt its structure.
2. Write the doc in 2–4 chunks (one `writeFile` if short; otherwise
   `writeFile` + appends via `editFile`). Before each chunk, re-read the
   supplying artifact(s) from disk.
3. House style throughout; self-contained per Rule 3.

## S7 — Verify

Run the checklist and record each result in 07-verification.md:
1. **Self-containment**: grep the doc for plan-artifact references —
   `plan/`, `appendix`, phase labels, task / requirement / gate IDs (adapt
   the patterns to the project's plan vocabulary; the `fix-comments` skill's
   `references/plan-artifacts.md` is a good pattern list when present).
   Required: zero hits (excluding legitimate technical terms).
2. **Fact re-check**: re-read the doc; for every concrete claim, confirm it
   against the 02/03 artifacts, and spot-check at least 3 claims directly
   against the source.
3. **Fix**: apply corrections; re-run the self-containment grep; re-read
   every edited region — edits are the usual source of doc defects
   (duplicate lines, broken numbering).
4. Record pass/fail per item; list residual gaps as open questions.

## Splitting guidance (large features)

- S2: one artifact per module group; one group = one pass of context.
- S3: split per flow if one pass cannot trace the whole path.
- S6: one chunk per 1–3 doc sections.
- After each artifact is written, the step is safe to compact.

## Final report

- doc path
- section list
- verification summary (self-containment result, facts checked, fixes applied)
- open questions
- user-framing corrections made, with the evidence
