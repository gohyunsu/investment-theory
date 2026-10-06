"""Build the GitHub Pages site and the matching standalone LaTeX guide.

The three content files are the single editorial source for both outputs.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [
    ("01-intro", "1부 · 투자와 금융자산", "투자의 구조"),
    ("02-risk-return", "2부 · 수익률과 위험", "불확실성의 측정"),
    ("03-two-assets", "3부 · 두 자산 포트폴리오", "분산과 최적화"),
]
SLIDE_RE = re.compile(r"^## (\d+)\. (.+)$", re.MULTILINE)
SUPPLEMENT_RE = re.compile(r"^## ([\w-]+/\d+) \| (.+)$", re.MULTILINE)
DEEP_DIVE_RE = re.compile(r"^## ([\w-]+/\d+) \| (.+)$", re.MULTILINE)
CASE_RE = re.compile(r"^## ([\w-]+/\d+) \| (.+)$", re.MULTILINE)
MATH_RE = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^$\n]+\$)")


def render_markdown(source: str) -> str:
    """Keep TeX untouched while Markdown handles surrounding prose."""
    formulas: list[str] = []

    def protect(match: re.Match[str]) -> str:
        token = f"MATHPLACEHOLDER{len(formulas):04d}END"
        formulas.append(match.group(0))
        return token

    result = markdown.markdown(MATH_RE.sub(protect, source), extensions=["extra"])
    for index, formula in enumerate(formulas):
        result = result.replace(f"MATHPLACEHOLDER{index:04d}END", html.escape(formula, quote=False))
    return result


def slides_from_markdown(path: Path, slug: str, chapter: str) -> list[dict]:
    source = path.read_text(encoding="utf-8")
    matches = list(SLIDE_RE.finditer(source))
    result = []
    for i, match in enumerate(matches):
        number = int(match.group(1))
        body = source[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(source)].strip()
        result.append({
            "id": f"{slug}/{number}",
            "chapter": slug,
            "chapterName": chapter,
            "page": number,
            "title": match.group(2),
            "image": f"assets/slides/{slug}-{number:02}.webp",
            "html": render_markdown(body),
            "raw": body,
        })
    if len(result) != 22 or [s["page"] for s in result] != list(range(1, 23)):
        raise ValueError(f"{path}: expected exactly 22 ordered slide sections")
    return result


def load_supplements() -> dict[str, dict]:
    source = (ROOT / "content/supplements.md").read_text(encoding="utf-8")
    matches = list(SUPPLEMENT_RE.finditer(source))
    result = {}
    for i, match in enumerate(matches):
        body = source[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(source)].strip()
        result[match.group(1)] = {"title": match.group(2), "raw": body, "html": render_markdown(body)}
    return result


def load_deep_dives() -> dict[str, str]:
    source = (ROOT / "content/deep-dives.md").read_text(encoding="utf-8")
    matches = list(DEEP_DIVE_RE.finditer(source))
    result = {}
    for i, match in enumerate(matches):
        key = match.group(1)
        if key in result:
            raise ValueError(f"Duplicate deep dive: {key}")
        body = source[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(source)].strip()
        if not body:
            raise ValueError(f"Empty deep dive: {key}")
        result[key] = body
    return result


def load_cases() -> dict[str, dict]:
    source = (ROOT / "content/questions-cases.md").read_text(encoding="utf-8")
    matches = list(CASE_RE.finditer(source))
    result = {}
    for i, match in enumerate(matches):
        key = match.group(1)
        if key in result:
            raise ValueError(f"Duplicate question and case: {key}")
        body = source[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(source)].strip()
        if not body:
            raise ValueError(f"Empty question and case: {key}")
        result[key] = {"title": match.group(2), "raw": body, "html": render_markdown(body)}
    return result


def tex_escape(text: str) -> str:
    translations = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
        "≈": r"\ensuremath{\approx}",
    }
    return "".join(translations.get(c, c) for c in text)


def tex_inline(text: str) -> str:
    chunks = MATH_RE.split(text)
    result = []
    for chunk in chunks:
        if chunk.startswith("$") and chunk.endswith("$"):
            result.append(chunk)
        else:
            escaped = tex_escape(chunk)
            escaped = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", escaped)
            result.append(escaped)
    return "".join(result)


def tex_body(source: str) -> str:
    blocks = re.split(r"\n\s*\n", source.strip())
    output = []
    for block in blocks:
        if block.startswith("$$") and block.endswith("$$"):
            output.append("\\[\n" + block[2:-2].strip() + "\n\\]")
        elif block.startswith("### "):
            title, _, rest = block.partition("\n")
            output.append("\\paragraph{" + tex_inline(title[4:]) + "}\n" + tex_inline(rest))
        elif block.startswith("- "):
            items = ["\\item " + tex_inline(line[2:]) for line in block.splitlines() if line.startswith("- ")]
            output.append("\\begin{itemize}\n" + "\n".join(items) + "\n\\end{itemize}")
        else:
            output.append(tex_inline(" ".join(block.splitlines())) + "\n\\par")
    return "\n\n".join(output)


def build_tex(slides: list[dict]) -> None:
    preamble = r"""\documentclass[11pt,a4paper]{article}
\usepackage{fontspec}
\IfFontExistsTF{Malgun Gothic}{\setmainfont{Malgun Gothic}}{\setmainfont{Noto Sans CJK KR}}
\XeTeXlinebreaklocale "ko"
\XeTeXlinebreakskip = 0pt plus 1pt
\usepackage{amsmath,amssymb,bm}
\setlength{\textwidth}{162mm}
\setlength{\textheight}{242mm}
\setlength{\oddsidemargin}{-1.4mm}
\setlength{\evensidemargin}{-1.4mm}
\setlength{\topmargin}{-12mm}
\renewcommand{\contentsname}{목차}
\emergencystretch=3em
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.55em}
\setcounter{tocdepth}{2}
\title{주식, 채권, 파생금융상품 1: 이론\\\large 슬라이드별 학습 가이드}
\author{}
\date{}
\begin{document}
\maketitle
\tableofcontents
\clearpage
"""
    parts = [preamble]
    current = None
    for slide in slides:
        if slide["chapter"] != current:
            if current is not None:
                parts.append("\\clearpage\n")
            current = slide["chapter"]
            parts.append("\\section{" + tex_escape(slide["chapterName"]) + "}\n")
        parts.append("\\subsection{슬라이드 " + str(slide["page"]) + ": " + tex_escape(slide["title"]) + "}\n")
        parts.append(tex_body(slide["raw"]) + "\n")
        case = slide["case"]
        parts.append("\\paragraph{" + tex_inline(case["title"]) + "}\n")
        parts.append(tex_body(case["raw"]) + "\n")
        if slide.get("supplement"):
            parts.append("\\paragraph{" + tex_escape(slide["supplement"]["title"]) + "}\n")
            parts.append(tex_body(slide["supplement"]["raw"]) + "\n")
    parts.append("\\end{document}\n")
    (ROOT / "guide.tex").write_text("\n".join(parts), encoding="utf-8")



def main() -> None:
    slides = []
    for slug, name, _ in CHAPTERS:
        slides.extend(slides_from_markdown(ROOT / "content" / (slug + ".md"), slug, name))
    deep_dives = load_deep_dives()
    slide_ids = {slide["id"] for slide in slides}
    if set(deep_dives) != slide_ids:
        raise ValueError(f"Deep dives must cover every slide: missing={slide_ids-set(deep_dives)}, extra={set(deep_dives)-slide_ids}")
    for slide in slides:
        slide["raw"] += "\n\n" + deep_dives[slide["id"]]
        slide["html"] = render_markdown(slide["raw"])
    cases = load_cases()
    if set(cases) != slide_ids:
        raise ValueError(f"Questions and cases must cover every slide: missing={slide_ids-set(cases)}, extra={set(cases)-slide_ids}")
    for slide in slides:
        slide["case"] = cases[slide["id"]]
    supplements = load_supplements()
    if set(supplements) - {slide["id"] for slide in slides}:
        raise ValueError("A supplement points to a missing slide")
    for slide in slides:
        if slide["id"] in supplements:
            slide["supplement"] = supplements[slide["id"]]
    manifest = json.loads((ROOT / "assets/slide-manifest.json").read_text(encoding="utf-8"))
    assets = {item["path"] for item in manifest}
    if len(slides) != 66 or len(assets) != 66 or any(s["image"] not in assets for s in slides):
        raise ValueError("The guide and slide image manifest must align on all 66 pages")
    build_tex(slides)
    from site_builder import build_site
    build_site(ROOT, slides)
    print(f"Built {len(slides)} slide sections, guide.tex, data.json, home and chapter pages")


if __name__ == "__main__":
    main()
