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
\title{주식·채권·파생금융상품의 이론\\\large 슬라이드별 학습 가이드}
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
        if slide.get("supplement"):
            parts.append("\\paragraph{" + tex_escape(slide["supplement"]["title"]) + "}\n")
            parts.append(tex_body(slide["supplement"]["raw"]) + "\n")
    parts.append("\\end{document}\n")
    (ROOT / "guide.tex").write_text("\n".join(parts), encoding="utf-8")


def build_site(slides: list[dict]) -> None:
    data = [{
        k: (v.replace(r"\boldsymbol", r"\mathbf") if k == "html" else v)
        for k, v in slide.items() if k not in ("raw", "supplement")
    } | ({
        "supplement": {
            "title": slide["supplement"]["title"],
            "html": slide["supplement"]["html"].replace(r"\boldsymbol", r"\mathbf"),
        }
    } if slide.get("supplement") else {}) for slide in slides]
    (ROOT / "data.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    references = [
        ("미국 SEC · 투자와 자산배분", "https://www.investor.gov/introduction-investing/getting-started/asset-allocation"),
        ("미국 SEC · 투자 위험의 종류", "https://www.investor.gov/introduction-investing/investing-basics/what-risk"),
        ("미국 재무부 · 단기국채와 가격", "https://www.treasurydirect.gov/marketable-securities/understanding-pricing/"),
        ("FINRA · 증거금 거래의 위험", "https://www.finra.org/investors/investing/investment-products/stocks"),
        ("한국거래소 · 코스피200 선물", "https://global.krx.co.kr/contents/GLB/02/0201/0201040201/GLB0201040201.jsp"),
        ("Markowitz (1952) · Portfolio Selection", "https://doi.org/10.1111/j.1540-6261.1952.tb01525.x"),
        ("미국 연방준비제도 · 위험 프리미엄", "https://www.federalreserve.gov/publications/may-2021-asset-valuations.htm"),
    ]
    refs = "".join(f'<li><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(name)}</a></li>' for name, url in references)
    (ROOT / "index.html").write_text(f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>주식·채권·파생금융상품의 이론 | 학습 가이드</title>
<meta name="description" content="수익률, 위험, 두 자산 포트폴리오를 66개 슬라이드 흐름에 따라 설명하는 금융투자 이론 가이드.">
<link rel="stylesheet" href="style.css"><link rel="icon" href="favicon.svg" type="image/svg+xml">
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre']}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<script defer src="app.js"></script></head>
<body><a class="skip" href="#main">본문으로 이동</a>
<header class="top"><a class="brand" href="#01-intro/1"><span class="mark">F</span><span>금융투자 이론<br><small>STUDY ATLAS</small></span></a><span class="top-right">66 slides · 3 chapters</span></header>
<div class="layout"><aside class="sidebar"><div class="sidebar-intro"><span class="eyebrow">COURSE GUIDE</span><h1>투자에서<br>포트폴리오까지</h1><p>개념의 출발점부터 수식의 유도와 경제학적 직관까지.</p></div><label class="search-label" for="search">슬라이드 찾기</label><input id="search" type="search" placeholder="예: VaR, 공분산, 샤프비율" autocomplete="off"><nav id="nav" aria-label="슬라이드 목록"></nav><div class="sidebar-footer"><a href="guide.pdf">PDF 가이드</a><a href="guide.tex">TeX 원고</a><button id="refs-open" type="button">더 읽을 자료</button></div></aside>
<main id="main" tabindex="-1"><div class="progress"><div id="progress-fill"></div></div><div id="reader"></div><div class="bottom-nav"><button id="previous" type="button">← 이전</button><span id="position"></span><button id="next" type="button">다음 →</button></div></main></div>
<dialog id="references"><div class="dialog-head"><div><span class="eyebrow">REFERENCES</span><h2>더 읽을 자료</h2></div><button id="refs-close" aria-label="닫기">×</button></div><p>개념과 제도의 배경을 더 깊이 살펴볼 수 있는 공식 자료와 원전이다.</p><ul>{refs}</ul></dialog>
</body></html>""", encoding="utf-8")


def main() -> None:
    slides = []
    for slug, name, _ in CHAPTERS:
        slides.extend(slides_from_markdown(ROOT / "content" / (slug + ".md"), slug, name))
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
    build_site(slides)
    print(f"Built {len(slides)} slide sections, guide.tex, data.json and index.html")


if __name__ == "__main__":
    main()
