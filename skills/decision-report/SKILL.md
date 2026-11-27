---
name: decision-report
description: >-
  Write a decision/analysis report that evaluates alternatives against explicit
  criteria and recommends a way forward. Encodes the proven skeleton:
  Problem, Background, Evaluation criteria, Alternatives (all scored against the
  same fixed criteria, depth proportional to seriousness), Summary, with the
  recurring grammar of aspect tables, symptom/cause tables, step procedures,
  verdict headings and paired pro/con bullets. Works for English or Swedish
  reports. Use when the user asks to write a report, options analysis,
  evaluation document, trade-off study, or a change-of-way-of-working proposal,
  or to structure/rewrite an existing analysis document.
  Triggers on: decision report, analysis report, options analysis, alternatives
  evaluation, evaluation criteria, trade-off study, write report, change
  proposal, decision-report.
version: 1.0.0
---

# Decision Report

## When to Use

- Writing a report that compares options/alternatives and recommends one.
- Structuring or rewriting an existing analysis/decision document.
- Documenting a proposed change of way-of-working (process, repo topology, tooling).
- NOT for: design docs of implemented features (use design-doc), implementation
  plans (use implementation-plan), or plain status reports.

## Core Principle

The report exists so the reader can challenge the evaluation. Every judgment
must trace to explicit, written-down criteria, and every alternative —
including "do nothing" — is scored against that same fixed set.

## Rules

1. Fix the evaluation criteria BEFORE writing any alternative. Number them,
   give each a one-line project-specific definition, and define one scoring
   scale (e.g. OK/NOK or Strong/Medium/Weak). State why the criteria are
   written down.
2. Score every alternative against the SAME criteria list. Never invent or
   drop criteria during evaluation.
3. Match depth to seriousness: discarded options get Pro/Con bullets only;
   shortlisted options get a summary table plus one subsection per criterion;
   the leading option additionally gets concrete artifacts (config, directory
   trees) and a proposed concrete structure with open questions marked inline.
4. Always include "do nothing" as alternative 1.
5. Use the recurring grammar (tables, verdict headings, paired bullet blocks).
   Templates in references/patterns.md.
6. End with a summary: bulleted, quantified takeaways plus one comparison
   table covering ALL alternatives.
7. One heading level per depth. Numbering supports hierarchy, never replaces it.
   Defect list in references/quality-checklist.md.

## Workflow

1. Gather the problem, affected architecture and concrete evidence (numbers,
   sizes, incidents, dated notes). Protocol in references/structure.md.
2. Draft §1 Problem: state tables, symptom/cause tables, current-workflow step tables.
3. Draft §2 Additional Background: only facts the criteria and options depend on.
4. Define criteria, scoring scale and desired end state (§3).
5. Enumerate alternatives; evaluate each per Rule 3 (§4).
6. Write §5 Summary of Alternatives: takeaways + full comparison table.
7. Verify against references/quality-checklist.md before delivering.

## References

- references/structure.md — section-by-section skeleton with content guidance
- references/patterns.md — table templates, verdict vocabulary, depth rules
- references/quality-checklist.md — defects to avoid and delivery checklist
