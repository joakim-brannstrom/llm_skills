# Decision Report — Section-by-Section Structure

Five-part macro skeleton. Sections 1-3 prepare the evaluation, section 4 is the
payload, section 5 decides. Adapt section names to the project language; keep
the order.

## 0 Header

- Title carrying the date of the decision being analyzed: `YYYY-MM-DD <topic>`.
- Program/project line and a full document date on the next lines.
- Table of contents as a nested list WITHOUT page numbers (page numbers rot and
  drift); keep entries in sync with the actual headings.

## 1 Problem

Goal: make the reader feel the problem before any option is shown.

- 1.1 Background — one state table with a row per component of the current
  situation: `| Aspect | Description | Problem |`. When a fact changed after
  drafting, put a dated inline note in the affected cell (convention and
  rationale: "Inline notes" in references/patterns.md).
- 1.2..1.n Problem mechanisms — one block per concrete pain. Each block:
  a `| Symptom | Cause |` table, then numbered step-by-step procedures of how
  the process works today and how the reference/benchmark (e.g. a governing
  process or another project) does it. Keep steps concrete and executable.
- 1.3 "What is X" — if a central term is ambiguous, define it: current
  situation table, then the intended state as numbered ground principles plus a
  `| Step | Description |` procedure table, then consequence subsections
  ("Consequences of <behavior>").

## 2 Additional Background

Facts the reader must agree on BEFORE judging options. Include only what the
criteria or the options depend on. Typical blocks:

- Technology constraints: one block per technology — what the tooling handles
  well/poorly, with measured examples (sizes, line counts, durations).
- Prior experience / case study: what was tried before, what it contained,
  what worked (bullets), what failed (bullets), how people adapted anyway.
  Lessons from adaptations are as valuable as the failures.
- Neutral definitions of candidate patterns (one short paragraph each).
- A generic pro/con catalog of the main pattern under discussion, one
  sub-heading per pro and per con. This becomes reusable ammunition for §4.

## 3 Evaluation Criteria

- Numbered criteria list; each criterion gets a one-sentence definition in the
  project's own terms, never generic boilerplate. 4-7 criteria is the sweet spot.
- State explicitly why they are written down: so the reader can see how
  alternatives were evaluated, why, and challenge the evaluation.
- Define the scoring scale and how to read it (e.g. OK/NOK, Strong/Medium/Weak).
- 3.1 Desired end state: short bullet list of what "good" looks like. It must
  not contradict the criteria.

## 4 Alternatives

Order: "1. Do nothing" first, then increasing ambition/effort.

For each alternative:

- One-paragraph statement: what changes, for whom, what stays.
- Evaluation depth by seriousness (rules in references/patterns.md):
  - Discarded: Pro/Con bullets only.
  - Shortlisted: intro + summary table `| Criterion | Assessment |` + one
    subsection per criterion, each with verdict heading and paired bullets.
  - Leading: additionally concrete artifacts in code blocks (config, directory
    trees, example commands), a proposed concrete structure with open
    questions marked inline, and `| Criterion | Assessment | Comment |`.
- Any option with a new risk profile gets "New risks specific to this context".

## 5 Summary of Alternatives

- 3-6 bullets of executive takeaways, quantified where possible
  ("reduces the number of repos from ~200 to ~5").
- One comparison table covering ALL alternatives:
  `| Alternative | Strengths | Risks / Limitations | Comment / Usefulness |`.
  If rows are tall, split into several tables with identical column semantics.
- If a recommendation is intended, state it and name the runner-up with the
  decisive reason.
