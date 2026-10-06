"""Render one web image per page of the local course PDFs.

Run from the repository root with a private source directory as argument.
The PDFs and temporary raster files are never copied into this repository.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


SOURCES = [
    ("01-intro", "01_intro.pdf"),
    ("02-risk-return", "02_risk-return.pdf"),
    ("03-two-assets", "03_two-asset-portfolios.pdf"),
]


def page_count(pdf: Path) -> int:
    result = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True)
    return int(next(line.split(":", 1)[1].strip() for line in result.stdout.splitlines() if line.startswith("Pages:")))


def main() -> None:
    source = Path(sys.argv[1]).resolve()
    destination = Path("assets/slides")
    destination.mkdir(parents=True, exist_ok=True)
    manifest = []
    for slug, name in SOURCES:
        pdf = source / name
        count = page_count(pdf)
        with tempfile.TemporaryDirectory() as temporary:
            stem = Path(temporary) / "slide"
            subprocess.run(["pdftoppm", "-f", "1", "-l", str(count), "-scale-to-x", "1600", "-scale-to-y", "-1", "-png", str(pdf), str(stem)], check=True)
            images = sorted(Path(temporary).glob("slide-*.png"))
            if len(images) != count:
                raise RuntimeError(f"{name}: expected {count} pages, rendered {len(images)}")
            for number, path in enumerate(images, 1):
                target = destination / f"{slug}-{number:02}.webp"
                with Image.open(path) as image:
                    image.convert("RGB").save(target, "WEBP", quality=88, method=6)
                manifest.append({"chapter": slug, "page": number, "path": str(target).replace("\\", "/")})
        print(f"{name}: {count} pages")
    Path("assets/slide-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
