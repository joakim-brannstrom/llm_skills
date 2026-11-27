#!/usr/bin/env python3
"""Check PPTX structure and optionally verify unchanged MarkItDown output."""

import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("presentation", type=Path)
    parser.add_argument("--markdown", type=Path, help="Raw MarkItDown .md file to verify")
    parser.add_argument("--expect-slides", type=int, help="Required slide count")
    parser.add_argument(
        "--allow-out-of-bounds",
        action="store_true",
        help="Downgrade canvas-bound violations to warnings for deliberate bleed",
    )
    args = parser.parse_args()

    source = args.presentation.resolve()
    if not source.is_file():
        parser.error(f"presentation not found: {source}")
    if args.expect_slides is not None and args.expect_slides < 1:
        parser.error("--expect-slides must be positive")

    try:
        from pptx import Presentation
    except ImportError:
        parser.error("python-pptx is required")

    errors = []
    warnings = []
    try:
        deck = Presentation(source)
    except Exception as error:
        print(f"FAIL: cannot reopen {source}: {error}", file=sys.stderr)
        return 1

    slide_count = len(deck.slides)
    if slide_count == 0:
        errors.append("the deck contains no slides")
    if args.expect_slides is not None and slide_count != args.expect_slides:
        errors.append(f"expected {args.expect_slides} slides, found {slide_count}")

    out_of_bounds = []
    for slide_index, slide in enumerate(deck.slides, 1):
        for shape in slide.shapes:
            outside = (
                shape.left < 0
                or shape.top < 0
                or shape.left + shape.width > deck.slide_width
                or shape.top + shape.height > deck.slide_height
            )
            if outside:
                out_of_bounds.append(f"slide {slide_index}: {shape.name}")
    if out_of_bounds:
        destination = warnings if args.allow_out_of_bounds else errors
        destination.extend(f"shape outside slide canvas: {item}" for item in out_of_bounds)

    if args.markdown:
        markdown = args.markdown.resolve()
        if not markdown.is_file():
            errors.append(f"Markdown file not found: {markdown}")
        else:
            try:
                from markitdown import MarkItDown
                generated = MarkItDown().convert(source).text_content
            except Exception as error:
                errors.append(f"MarkItDown conversion failed: {error}")
            else:
                actual = markdown.read_text(encoding="utf-8")
                if actual != generated:
                    errors.append(
                        f"{markdown} differs from raw MarkItDown output for the current PPTX"
                    )

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"PASS: {source}")
    print(f"Slides: {slide_count}")
    print("Canvas bounds: " + ("warnings only" if args.allow_out_of_bounds else "valid"))
    if args.markdown:
        print(f"Markdown: unchanged MarkItDown output ({args.markdown})")
    print("Note: structural validation is not visual validation.")


if __name__ == "__main__":
    raise SystemExit(main())
