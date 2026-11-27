---
name: presentation-authoring
description: Create reproducible PowerPoint decks with python-pptx, extract Markdown with MarkItDown, render slides to PDF/PNG, and perform structural, textual, and vision-based QA with iterative repairs. Use when creating, revising, converting, rendering, inspecting, or validating presentations. Triggers on: presentation, PowerPoint, PPTX, slide deck, slides, MarkItDown presentation, render slides, presentation validation, visual QA
version: 1.0.0
---

# Presentation Authoring

## When to Use

Use this skill for slide-deck requests where content must be authored, converted, or checked. It covers both creation and validation; visual validation is optional only when the user does not request it. Do not use it for unrelated document-generation tasks.

## Core Principle

Treat authoring, text extraction, rendering, and visual inspection as separate stages. `python-pptx` authors the PPTX; MarkItDown extracts its text; LibreOffice and Poppler render it; image inspection evaluates what the audience can actually see. Never equate a valid PPTX or extracted Markdown with a visually valid deck.

## Rules

- Read the brief, existing source files, and attachments before choosing content or changing a deck.
- Keep a reproducible Python generator with the delivered PPTX. Do not hand-edit binary output when the generator can be corrected.
- Use one clear message per slide and keep essential information as real text rather than screenshots.
- Verify code and factual claims before placing them on slides.
- Do not install dependencies without authorization. Name missing tools or request an approved Dockerfile change.
- Do not claim visual inspection unless rendered output was opened with vision support.
- After a source change, regenerate dependent artifacts and repeat the relevant checks.
- State the renderer used and any font substitution or unresolved viewer-specific limitation.

## Workflow

1. **Scope the deck**: establish topic, audience, purpose, tone, aspect ratio, and approximate length. Ask when ambiguity materially matters; otherwise choose conservative defaults and disclose assumptions.
2. **Check capabilities**: inspect Python dependencies and locate `libreoffice`/`soffice`, `pdftoppm`, and `pdftotext` before planning the rendering route.
3. **Outline before styling**: draft slide titles, key messages, supporting content, and visual patterns. Review source material for accuracy and completeness.
4. **Author reproducibly**: build the deck with `python-pptx`, using shared layout, color, type, spacing, and shape helpers. Save both generator and PPTX.
5. **Run nonvisual checks**: reopen the PPTX, verify slide count and shape bounds, then run MarkItDown when a Markdown edition or text QA is useful. Inspect extracted reading order and completeness.
6. **Render**: convert PPTX to PDF and each page to PNG; create a contact sheet. Use writable cache/profile locations in restricted containers.
7. **Inspect with vision**: review the contact sheet for consistency and every full-resolution slide for clipping, overflow, overlap, wrapping, glyphs, contrast, alignment, spacing, and code readability.
8. **Repair and repeat**: correct the source generator, regenerate, rerender, and reinspect changed slides plus the full-deck overview. Resolve uncertain OCR using enlarged crops and PDF text rather than guessing.
9. **Finish honestly**: report actual checks performed and distinguish structural, extraction, and rendered-visual QA.

Detailed commands and decision guidance are in `references/workflow.md`; the inspection rubric is in `references/visual-qa.md`.

## Output Format

Return the PPTX and generator paths, plus requested Markdown or rendered artifacts. Summarize slide count, validation performed, fixes made, and remaining caveats. For visual QA, provide the PDF, PNG/contact-sheet paths, and a concise slide-by-slide or overall verdict. Do not bury failures or silently omit unperformed checks.

## References

- `references/workflow.md`: end-to-end protocol, dependency checks, and commands
- `references/visual-qa.md`: vision checklist, repair rules, and reporting guidance
- `scripts/validate_presentation.py`: structural and raw-Markdown verification
- `scripts/render_presentation.py`: PDF/PNG rendering, PDF text, and contact-sheet generation
