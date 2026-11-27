# Presentation workflow

Resolve `SKILL_DIR` as the directory containing this skill's `SKILL.md`. Run deck commands from the user's output directory.

## 1. Define the deliverable

Capture the topic, audience, desired takeaway, tone, slide-count range, aspect ratio, required branding, source assets, and requested output formats. Inspect attachments and existing decks before authoring. If details are absent and do not block useful work, state assumptions such as a concise 16:9 deck rather than stalling.

Decide whether MarkItDown is needed. It produces a Markdown extraction from an existing presentation; it is not the slide-authoring library.

## 2. Check tools without changing the environment

```sh
python3 -c "import pptx; from markitdown import MarkItDown"
command -v libreoffice || command -v soffice
command -v pdftoppm
command -v pdftotext
```

Typical Python requirements are `python-pptx` and MarkItDown with PPTX support. On Debian, the rendering tools come from `libreoffice-impress` and `poppler-utils`; useful font packages include `fonts-dejavu-core` and `fonts-liberation`. Package names vary by platform. If anything is missing, report the exact requirement or modify an approved image definition—do not install opportunistically.

## 3. Build an outline and design system

For each slide, write its title, single takeaway, essential content, and visual form: title, two-column, cards, process, code, table, or checklist. Remove repetition and content that does not support the takeaway. Verify examples and commands independently.

Choose a small token set before implementation:

- canvas and outer margins;
- background, panel, primary-text, muted-text, and accent colors;
- heading, body, caption, and monospaced font roles;
- standard title position, content grid, card padding, and footer.

Use meaningful reading order, high contrast, deliberate whitespace, and text sizes suitable for projection. Avoid using screenshots for information that should remain searchable or editable. Prefer shortening copy or widening a region over repeatedly shrinking text.

## 4. Generate and run structural checks

Write `create_presentation.py` using `python-pptx`. Centralize helpers for text boxes, cards, code blocks, bullets, and recurring slide furniture. Save a 16:9 PPTX unless the brief specifies another format.

```sh
python3 create_presentation.py
python3 "$SKILL_DIR/scripts/validate_presentation.py" deck.pptx
```

The validator checks that the deck reopens, has slides, and keeps shapes within the canvas. If deliberate bleed is part of the design, use `--allow-out-of-bounds` and inspect those regions visually. Structural checks cannot establish visual quality.

## 5. Extract and inspect Markdown when useful

```sh
python3 -m markitdown deck.pptx -o deck.md
python3 "$SKILL_DIR/scripts/validate_presentation.py" deck.pptx --markdown deck.md
```

Review slide order, titles, essential text, code, and reading order. The Markdown validator confirms that the file is the unchanged output from the current PPTX. If a human-edited Markdown edition is intended, compare its content semantically instead of requiring byte equality.

Never use extracted Markdown to assess font size, clipping, contrast, or visual overlap.

## 6. Render the deck

```sh
python3 "$SKILL_DIR/scripts/render_presentation.py" deck.pptx \
  --output-dir rendered --dpi 144
```

The helper:

- selects `libreoffice` or `soffice`;
- creates temporary writable home, cache, and LibreOffice profile directories;
- exports `rendered/deck.pdf`;
- writes full-slide `slide-N.png` images;
- removes stale numbered PNGs from earlier runs;
- writes `pdf-text.txt` when `pdftotext` is available;
- creates `contact-sheet.png` when Pillow is available.

Check the page/image count against the PPTX slide count. Open the images with the available vision tool; generating them is not itself visual inspection.

## 7. Inspect and repair

Apply `references/visual-qa.md`. Use the contact sheet for deck-wide consistency and full-resolution images for detailed checks. Use `pdftotext -layout` to identify unexpected wrapping and enlarged image crops for uncertain code or spelling.

Classify failures before editing:

- missing or incorrect content: repair the outline/source data;
- clipping, wrapping, or overlap: adjust copy, geometry, or type scale in the generator;
- inconsistent spacing or alignment: fix shared layout helpers/tokens;
- missing glyphs or suspicious font metrics: check installed fonts and substitutions;
- extraction problems: inspect source text and shape order separately from visual layout.

Regenerate and rerun structural checks, Markdown extraction, rendering, and visual review after relevant edits. Do not accept a new render solely because the previous issue disappeared; check for regressions.

## 8. Complete the handoff

Include the final PPTX, source generator, and requested derived artifacts. For a visually validated deck, include the PDF, contact sheet, individual PNG directory, and validation summary. Report what was actually run, remaining warnings, renderer version if relevant, and font substitutions. Note that LibreOffice rendering does not guarantee pixel-identical Microsoft PowerPoint output.
