"""Compile the generated Korean guide to a distributable PDF."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "_build"


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / "tools/build.py")], cwd=ROOT, check=True)
    command = ["xelatex"]
    if os.name == "nt":
        command.append("-disable-installer")
    command += [
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "-output-directory",
        str(BUILD),
        str(ROOT / "guide.tex"),
    ]
    for pass_number in (1, 2):
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        if result.returncode:
            print(result.stdout[-6000:].decode(errors="replace").encode("ascii", "backslashreplace").decode())
            raise RuntimeError(f"XeLaTeX pass {pass_number} failed")
    log = (BUILD / "guide.log").read_text(encoding="utf-8", errors="replace")
    problems = [line for line in log.splitlines() if "Missing character:" in line or "LaTeX Error:" in line or "Overfull \\hbox" in line]
    if problems:
        raise RuntimeError("LaTeX layout diagnostics:\n" + "\n".join(problems[:20]))
    shutil.copy2(BUILD / "guide.pdf", ROOT / "guide.pdf")
    info = subprocess.run(["pdfinfo", str(ROOT / "guide.pdf")], capture_output=True, text=True, check=True)
    pages = next(int(line.split(":", 1)[1].strip()) for line in info.stdout.splitlines() if line.startswith("Pages:"))
    if pages < 10:
        raise RuntimeError(f"PDF unexpectedly short: {pages} pages")
    print(f"Compiled guide.pdf ({pages} pages)")


if __name__ == "__main__":
    main()
