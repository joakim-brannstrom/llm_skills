#!/usr/bin/env python3
"""Render a PPTX to PDF, full-slide PNGs, PDF text, and a contact sheet."""

import argparse
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile


def run(command, **kwargs):
    print("+", shlex.join(str(part) for part in command), flush=True)
    subprocess.run([str(part) for part in command], check=True, **kwargs)


def slide_number(path):
    match = re.fullmatch(r"slide-(\d+)\.png", path.name)
    return int(match.group(1)) if match else -1


def create_contact_sheet(images, destination):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Pillow is unavailable; skipping contact-sheet.png", file=sys.stderr)
        return

    columns = 2 if len(images) > 1 else 1
    thumb_width = 768
    margin = 16
    label_height = 36
    with Image.open(images[0]) as first:
        thumb_height = round(thumb_width * first.height / first.width)
    rows = (len(images) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (
            columns * thumb_width + (columns + 1) * margin,
            rows * (thumb_height + label_height + margin) + margin,
        ),
        "#D8DDE6",
    )
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(images):
        with Image.open(path) as source:
            image = source.convert("RGB")
            image.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        x = margin + (index % columns) * (thumb_width + margin)
        y = margin + (index // columns) * (thumb_height + label_height + margin)
        sheet.paste(image, (x, y))
        draw.text((x + 6, y + thumb_height + 10), f"Slide {index + 1}", fill="#111827")
    sheet.save(destination)


def positive_dpi(value):
    dpi = int(value)
    if dpi <= 0:
        raise argparse.ArgumentTypeError("DPI must be positive")
    return dpi


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("presentation", type=Path, help="Input .pptx file")
    parser.add_argument("--output-dir", type=Path, default=Path("rendered"))
    parser.add_argument("--dpi", type=positive_dpi, default=144)
    args = parser.parse_args()

    source = args.presentation.resolve()
    if not source.is_file():
        parser.error(f"presentation not found: {source}")
    if source.suffix.lower() != ".pptx":
        parser.error("the input must be a .pptx file")

    office = shutil.which("libreoffice") or shutil.which("soffice")
    if not office:
        parser.error("LibreOffice is required (libreoffice or soffice was not found)")
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        parser.error("pdftoppm is required (normally provided by poppler-utils)")

    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for old_image in output.iterdir():
        if old_image.is_file() and slide_number(old_image) >= 1:
            old_image.unlink()

    with tempfile.TemporaryDirectory(prefix="presentation-render-") as temporary:
        temp = Path(temporary)
        home = temp / "home"
        cache = temp / "cache"
        profile = temp / "libreoffice-profile"
        for directory in (home, cache, profile):
            directory.mkdir()
        environment = os.environ.copy()
        environment["HOME"] = str(home)
        environment["XDG_CACHE_HOME"] = str(cache)
        run(
            [
                office,
                f"-env:UserInstallation={profile.as_uri()}",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                output,
                source,
            ],
            env=environment,
        )

    pdf = output / f"{source.stem}.pdf"
    if not pdf.is_file() or pdf.stat().st_size == 0:
        raise RuntimeError(f"LibreOffice did not produce a nonempty PDF: {pdf}")

    run([pdftoppm, "-png", "-r", args.dpi, pdf, output / "slide"])
    images = sorted(
        (path for path in output.iterdir() if slide_number(path) >= 1),
        key=slide_number,
    )
    if not images:
        raise RuntimeError("pdftoppm completed without creating numbered slide PNGs")

    pdftotext = shutil.which("pdftotext")
    if pdftotext:
        run([pdftotext, "-layout", pdf, output / "pdf-text.txt"])

    contact_sheet = output / "contact-sheet.png"
    create_contact_sheet(images, contact_sheet)
    print(f"PDF: {pdf}")
    print(f"Slides: {len(images)}")
    print(f"Images: {output / 'slide-N.png'} ({args.dpi} DPI)")
    if contact_sheet.is_file():
        print(f"Contact sheet: {contact_sheet}")
    print("Open the images with vision support before claiming visual validation.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Rendering failed: {error}", file=sys.stderr)
        raise SystemExit(1)
