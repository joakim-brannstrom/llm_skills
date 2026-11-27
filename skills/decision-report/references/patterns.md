# Decision Report — Recurring Patterns (the document's grammar)

## Table templates

State/inventory (one row per component of the current situation):

| Aspect | Description | Problem |

Symptom analysis:

| Symptom | Cause |

Procedure (workflow or process, step by step):

| Step | Description |

Criteria evaluation, shallow:

| Criterion | Assessment |

Criteria evaluation, full:

| Criterion | Assessment | Comment |

Final comparison (one row per alternative):

| Alternative | Strengths | Risks / Limitations | Comment / Usefulness |

Table rules:
- One logical table = one table. Never split it into repeated header rows.
- Keep cells short; narrative goes in prose under the table.
- If a row needs nuance, add a Comment column instead of cramming cells.

## Verdict vocabulary

Pick ONE scale per report and use it everywhere:
- OK / NOK — criterion satisfied or not (fast, binary).
- Strong / Medium / Weak — graded; allow direction, e.g. "Strong -> Medium for
  <case>", "Medium -> Hard".
Never mix scales within one evaluation section.

Verdicts may be used AS headings, directly above the paired bullets for that
criterion, e.g. `### Assessment: Strong`.

## Paired bullet blocks

Every evaluation subsection ends with exactly two bullet lists:
- Advantages / Pro
- Limitations / Con

No third list. Neutral observations belong in the verdict heading or the
Comment column.

## Criteria as anchors

The §3 criteria list is the only scoring vocabulary. Reuse the exact criterion
names in every option's tables and subsection titles
(`4.3.3.1 Progressive introduction`, `4.4.1.2 Reproducibility`, ...). Copy the
names verbatim — do not paraphrase per section.

## Concrete artifacts

For shortlisted options show real fragments in code blocks:
- configuration files (build inputs, repo manifests),
- directory / repo trees,
- example commands.
Mark unknowns inline rather than silently deciding: "(own repo or shared with
X? choose)". Unresolved choices stay visible.

## Inline notes

When a fact changes after the report was drafted, do not silently rewrite the
original claim — add a dated note next to it: "Note YYYY-MM-DD: <what changed>".

Why dated notes:
- The title date and the facts drift apart while the report circulates; the
  date shows which statement was true at which point.
- Decision reports double as evidence later ("why did we choose this?"); dated
  notes keep that audit trail instead of destroying it.
- A reader sees at a glance where report and reality diverge.

Variant: in the published final version, fold corrections into the body and
record them in a revision table (revision, change, affected sections, author)
instead of leaving inline notes behind.

Also: open questions — leave an explicit question in the text, never bury it.

## Depth proportionality

| Option status | Treatment |
|---|---|
| Discarded | 1-paragraph description + Pro/Con bullets |
| Shortlisted | Summary criteria table + per-criterion subsections (verdict + paired bullets) |
| Leading | + concrete artifacts, proposed concrete structure, commented criteria table |

Depth is about the option's realistic chance of being chosen, not about how
much the author likes it.
