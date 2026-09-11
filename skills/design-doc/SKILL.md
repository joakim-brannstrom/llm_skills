---
name: design-doc
description: >-
  Write a self-contained big-brush design document for an implemented feature:
  what it is, why it exists, and how its internals interact (architecture,
  control flow, data flow, failure modes). Multi-step and compression-resilient:
  each step persists findings to numbered scratch artifacts that the next step
  re-reads from disk, so context compression never loses analysis. Use when asked
  to document a feature, write or update a design doc for existing code, or
  explain how a feature works at the architecture level. Triggers on: design doc,
  design document, write design doc, document feature, feature documentation,
  architecture doc, explain feature design, document this feature.
version: 0.1.0
---

# Design Doc

Write an engineering design document for a feature that already exists in code.
The source of truth is the **implementation at the target revision**; planning
documents supply only intent, and sibling docs supply only style.

## When to Use

- User asks for a design doc / architecture doc for an implemented feature
- User asks to document how a feature works for engineers
- Updating an existing design doc after the feature changed

## Core Principle

**Compression resilience via on-disk checkpoints.** Context is finite and will
be compacted mid-task. Every step writes its findings to a numbered artifact
under `scratch/<docslug>/` (NN-name.md), and every step starts by re-reading
the artifacts it depends on **from disk** — never from remembered context.
The final doc is written only from artifacts. If a step does not fit in one
pass, split it into sub-steps with their own artifacts.

## Rules

1. **Verify before asserting.** No name, constant, threshold, default, or
   ordering may appear in an artifact or the doc without a grep/read that
   confirmed it this session. Record the anchor (file:line) in the artifact.
2. **Big brush, not a code tour.** Architecture, control flow, data flow,
   failure modes, invariants. Code references = module names + a few
   identifiers. No line-by-line walkthroughs.
3. **Self-contained.** Zero references to plan artifacts (plan files, task /
   requirement / phase IDs). Distill intent into prose. Where the
   implementation deviates from the plan, the doc states the implemented
   behavior — the code wins.
4. **House style.** Read 2–3 sibling docs in the target directory and mirror
   their structure, depth, and cross-reference style (S4).
5. **Push back with evidence.** If the user's framing of the feature
   contradicts the source, correct it in the final report; the code decides
   the doc's content.

## Workflow

Full protocol in `references/workflow.md`. Scratch dir: `scratch/<docslug>/`.

| Step | Artifact | Answers |
|------|----------|---------|
| S0 Scope | 00-scope.md | Feature, revision, doc path, style sources, constraints |
| S1 Intent | 01-intent.md | What and why; goals, non-goals, core design rules |
| S2 Implementation | 02a…02n-\<group\>.md | How each internal part works, per module group, verified |
| S3 Flows | 03-flows.md | Control flow + data flow: wiring, pipeline, query path, shutdown, error paths |
| S4 Conventions | 04-conventions.md | House style from sibling docs |
| S5 Outline | 05-outline.md | Sections; section→artifact map; facts to re-verify |
| S6 Write | target doc | Drafted from artifacts in 2–4 chunks, re-reading the supplying artifact per chunk |
| S7 Verify | 07-verification.md | Self-containment grep + fact re-check; fix, then re-verify |

## Output Format

Final report: doc path; section list; verification results (self-containment
pass/fail, facts checked, fixes applied); open questions; any user-framing
corrections made, with evidence.

## References

- Full step protocol, reading strategy, verification checklist:
  `references/workflow.md`
