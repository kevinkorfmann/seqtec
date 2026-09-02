#!/usr/bin/env python3
"""Fast, deterministic integrity checks for the SeqTec book and website.

These checks do not replace scientific review. They prevent a reviewed claim
from silently drifting out of sync with the edition metadata, chapter manifest,
or companion website.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.tex"
CHAPTER_DIR = ROOT / "chapters"
EXPECTED_CHAPTERS = [f"ch{i:02d}_" for i in range(1, 27)]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    errors = 0
    main_text = MAIN.read_text(encoding="utf-8")
    chapter_files = sorted(CHAPTER_DIR.glob("ch*.tex"))

    if len(chapter_files) != 26:
        fail(f"expected 26 numbered chapters, found {len(chapter_files)}")
        errors += 1

    for prefix in EXPECTED_CHAPTERS:
        matches = [path for path in chapter_files if path.name.startswith(prefix)]
        if len(matches) != 1:
            fail(f"expected exactly one chapter matching {prefix}, found {len(matches)}")
            errors += 1
            continue
        include = rf"\input{{chapters/{matches[0].stem}}}"
        if main_text.count(include) != 1:
            fail(f"{matches[0].name} is not included exactly once in main.tex")
            errors += 1

    labels: dict[str, Path] = {}
    for path in [MAIN, *chapter_files]:
        text = path.read_text(encoding="utf-8")
        for label in re.findall(r"\\label\{([^}]+)\}", text):
            if label in labels:
                fail(f"duplicate label {label!r} in {labels[label].name} and {path.name}")
                errors += 1
            labels[label] = path

    if "Version 2" not in main_text:
        fail("main.tex does not identify the Version 2 edition")
        errors += 1

    preface = (CHAPTER_DIR / "preface.tex").read_text(encoding="utf-8")
    if "eight parts" not in preface.lower():
        fail("preface must describe the book's eight parts")
        errors += 1

    # Guard the known NovaSeq arithmetic error: a 30x human genome is roughly
    # 90 Gb, or about 300 million PE150 clusters, not 30 million read pairs.
    experimental = (CHAPTER_DIR / "ch22_experimental_design.tex").read_text(
        encoding="utf-8"
    )
    forbidden = "330 WGS samples at 30$\\times$ coverage"
    if forbidden in experimental:
        fail("ch22 contains the disproven 330-sample NovaSeq multiplexing claim")
        errors += 1

    if errors:
        print(f"Verification failed with {errors} error(s).", file=sys.stderr)
        return 1
    print(f"Source integrity passed: {len(chapter_files)} chapters, {len(labels)} labels.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
