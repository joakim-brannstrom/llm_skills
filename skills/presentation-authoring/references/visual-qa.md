# Visual QA rubric

## Inspection sequence

1. Confirm that every PPTX slide has a corresponding rendered PNG and that image dimensions are consistent.
2. Inspect the contact sheet for sequence, visual rhythm, consistency, dense slides, and obvious outliers.
3. Open every slide at full resolution. A contact sheet alone is insufficient for detailed approval.
4. Reinspect every changed slide and the final contact sheet after repairs.
5. Use targeted crops for small code, filenames, symbols, footers, and suspected clipping.

## Per-slide checklist

Evaluate only visible evidence:

- **Boundaries**: text and shapes are not clipped by the slide edge or their containers.
- **Flow**: titles, body copy, bullets, code, captions, and graphics do not overlap.
- **Wrapping**: line breaks look intentional; words, filenames, and extensions are not split awkwardly.
- **Typography**: fonts render cleanly, symbols and arrows are correct, and code is legible.
- **Contrast**: text remains readable against its immediate background.
- **Alignment**: repeated elements share margins, baselines, padding, and spacing.
- **Hierarchy**: the slide title and main takeaway are clear; secondary content does not compete excessively.
- **Balance**: whitespace appears deliberate and content is neither cramped nor lost in empty space.
- **Content fidelity**: no characters, lines, bullets, or commands disappeared during rendering.

Record slide number, symptom, suspected source cause, proposed repair, and post-repair result. Distinguish a definite failure from a subjective design suggestion.

## Resolve uncertain evidence

Vision output can misread small text. Before changing source content based on a suspected typo:

1. inspect an enlarged crop;
2. extract the corresponding PDF text;
3. compare against the generator or original brief.

If these sources disagree, preserve the correct source and report the uncertainty rather than introducing a typo. PDF text extraction confirms embedded text, not visual aesthetics; use it alongside, never instead of, image inspection.

Check substitutions when a requested font is unavailable, for example:

```sh
fc-match Aptos
fc-match "DejaVu Sans Mono"
```

Report the actual renderer and substitution. A LibreOffice pass does not prove pixel-identical output in Keynote or Microsoft PowerPoint.

## Repair rules

- Fix the generator, not only a derived artifact.
- Prefer shorter copy, wider containers, or layout changes before aggressive font reductions.
- Preserve minimum readable sizes and adequate line spacing.
- Change shared helpers for systemic issues rather than patching each slide inconsistently.
- Reextract Markdown when slide text changes.
- Rerender the entire deck after regeneration, while giving changed slides the closest visual review.

## Final status vocabulary

Use precise statuses:

- **Pass**: inspected rendered output and found no remaining visible defect at the reviewed resolution.
- **Pass with caveat**: no blocking defect, but viewer/font differences or another explicit limitation remain.
- **Fail**: one or more identified defects remain; list them.

A practical handoff summary is:

```text
Rendered with: <renderer/version>
Reviewed: <slide count> slides, contact sheet + full-resolution images
Result: <status>
Fixes: <material layout repairs>
Artifacts: <PPTX, PDF, PNG/contact-sheet paths>
Caveats: <font substitutions, unreviewed viewers, unresolved defects>
```
