"""Prepare an explicit allowlist of files for GitHub Pages."""
from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = (ROOT / "_site").resolve()
if TARGET.parent != ROOT.resolve():
    raise RuntimeError("Unexpected publication directory")

manifest = json.loads((ROOT / "assets/slide-manifest.json").read_text(encoding="utf-8"))
if len(manifest) != 66:
    raise RuntimeError("Expected exactly 66 slide images")

allowed = [
    "index.html",
    "favicon.svg",
    "style.css",
    "app.js",
    "data.json",
    "guide.pdf",
    "guide.tex",
    ".nojekyll",
]
allowed += [entry["path"] for entry in manifest]
if len(allowed) != len(set(allowed)):
    raise RuntimeError("Duplicate publication path")
for relative in allowed:
    source = (ROOT / relative).resolve()
    if not source.is_relative_to(ROOT.resolve()) or not source.is_file():
        raise RuntimeError(f"Invalid publication source: {relative}")
    if source.suffix.lower() in {".txt", ".jpg", ".jpeg"}:
        raise RuntimeError(f"Unexpected source format: {relative}")

if TARGET.exists():
    shutil.rmtree(TARGET)
TARGET.mkdir()
for relative in allowed:
    destination = TARGET / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, destination)
files = [path for path in TARGET.rglob("*") if path.is_file()]
if len(files) != len(allowed):
    raise RuntimeError("Published file count differs from allowlist")
print(f"Packaged {len(files)} public files; {len(manifest)} slide images")
