"""Build the public study site from the same slide records as the PDF guide."""
from __future__ import annotations

import html
import json
from pathlib import Path


CHAPTERS = [
    {
        "slug": "01-intro", "number": "01", "title": "투자와 금융자산",
        "tagline": "실물·금융자산과 투자관리",
        "intro": "투자는 현재의 자원을 불확실한 미래의 현금흐름과 교환하는 선택이다. 먼저 자산이 어떤 청구권을 뜻하는지, 주식·채권·파생상품의 현금흐름이 어떻게 다른지 살펴본다. 이후 투자자가 기대수익, 위험, 거래제약을 함께 고려해야 하는 이유를 연결한다.",
    },
    {
        "slug": "02-risk-return", "number": "02", "title": "수익률과 위험",
        "tagline": "보유기간 수익률·분포·손실",
        "intro": "가격 변화와 배당을 하나의 보유기간 수익률로 묶은 뒤, 확률분포의 평균과 분산으로 미래 성과를 표현한다. 표본으로 모수를 추정할 때의 한계, 여러 기간의 수익률 계산, 손실의 꼬리를 읽는 방법까지 차례로 이어진다.",
    },
    {
        "slug": "03-two-assets", "number": "03", "title": "두 자산 포트폴리오",
        "tagline": "분산투자·효율적 집합·접점",
        "intro": "자산을 둘로 나누면 기대수익은 비중의 가중평균이지만 위험은 공분산에 따라 달라진다. 이 차이에서 분산투자의 이익을 유도하고, 최소분산점과 효율적 프런티어를 거쳐 무위험자산을 포함한 최적 조합을 구한다.",
    },
]

REFERENCES = [
    ("미국 SEC · 자산배분과 분산투자", "https://www.investor.gov/introduction-investing/getting-started/asset-allocation"),
    ("미국 SEC · 분산투자의 한계", "https://www.investor.gov/introduction-investing/investing-basics/save-and-invest/diversify-your-investments"),
    ("미국 SEC · 투자 위험", "https://www.investor.gov/introduction-investing/investing-basics/what-risk"),
    ("미국 재무부 · 국채 가격과 금리", "https://www.treasurydirect.gov/marketable-securities/understanding-pricing/"),
    ("FINRA · 주식 투자", "https://www.finra.org/investors/investing/investment-products/stocks"),
    ("FINRA · 채권과 듀레이션", "https://www.finra.org/investors/investing/investment-products/bonds"),
    ("미국 SEC · 인덱스펀드의 비용과 추적오차", "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-26"),
    ("미국 재무부 · 물가연동국채(TIPS)", "https://www.treasurydirect.gov/marketable-securities/tips/"),
    ("한국거래소 · 코스피200 선물", "https://global.krx.co.kr/contents/GLB/02/0201/0201040201/GLB0201040201.jsp"),
    ("Markowitz (1952) · Portfolio Selection", "https://doi.org/10.1111/j.1540-6261.1952.tb01525.x"),
    ("미국 연방준비제도 · 위험 프리미엄", "https://www.federalreserve.gov/publications/may-2021-asset-valuations.htm"),
]


def e(value: str) -> str:
    return html.escape(str(value), quote=True)


def layout(prefix: str, title: str, description: str, content: str) -> str:
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(description)}"><title>{e(title)} · 주식, 채권, 파생금융상품 1: 이론</title>
<link rel="stylesheet" href="{prefix}style.css"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<script defer src="{prefix}app.js"></script></head>
<body data-prefix="{prefix}"><a class="skip" href="#main">본문으로 이동</a><div class="reading-progress" aria-hidden="true"></div>
<header class="site-header"><a class="brand" href="{prefix}index.html"><span class="brand-mark">∑</span><span>주식, 채권, 파생금융상품 1: 이론</span></a><span class="header-divider"></span><span class="header-subtitle">슬라이드별 학습 가이드</span><a class="pdf-link" href="{prefix}guide.pdf" download>PDF 가이드 ↓</a><button type="button" class="search-trigger" data-search-trigger aria-label="전체 검색 열기"><span>⌕</span> 검색 <kbd>/</kbd></button></header>
{content}
<dialog id="slide-dialog" class="slide-dialog"><button type="button" class="dialog-close" data-dialog-close aria-label="이미지 닫기">×</button><img alt="확대한 슬라이드"><p></p></dialog>
<dialog id="search-dialog" class="search-dialog"><div class="search-panel"><div class="search-input-row"><span>⌕</span><input type="search" id="search-input" placeholder="개념, 사례, 수식 검색" aria-label="전체 내용 검색"><button type="button" data-search-close aria-label="검색 닫기">×</button></div><div id="search-results" class="search-results"></div><p class="search-hint">슬라이드 제목과 설명을 함께 검색합니다. Esc로 닫기</p></div></dialog>
</body></html>'''


def footer(prefix: str) -> str:
    return f'<footer class="site-footer">주식, 채권, 파생금융상품 1: 이론 · 2026-2 <span><a href="{prefix}guide.tex">LaTeX 원고</a></span></footer>'


def home(slides: list[dict]) -> str:
    cards = []
    for i, chapter in enumerate(CHAPTERS):
        count = sum(s["chapter"] == chapter["slug"] for s in slides)
        cards.append(f'''<a class="overview-card card-{('blue','teal','amber')[i]}" href="lecture/{chapter['number']}.html"><div class="overview-card-top"><span>{chapter['number']}</span><span>{count}개 슬라이드</span></div><h3>{e(chapter['title'])}</h3><p>{e(chapter['tagline'])}</p><div class="card-arrow">학습하기 <span>↗</span></div></a>''')
    refs = ''.join(f'<li><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}</a></li>' for label, url in REFERENCES)
    content = f'''<main id="main" class="home-main"><section class="home-hero"><div class="eyebrow">주식, 채권, 파생금융상품 1: 이론</div><h1>투자의 원리부터<br><em>포트폴리오 선택까지</em></h1><p>금융자산의 현금흐름을 이해하고, 수익률과 위험을 측정한 뒤, 두 자산의 분산효과와 효율적인 투자 조합을 직접 유도한다. 각 슬라이드와 해설이 같은 자리에서 이어진다.</p><div class="hero-actions"><a class="primary-button" href="lecture/01.html">처음부터 읽기 <span>→</span></a><a class="pdf-link" href="guide.pdf" download>PDF 내려받기 ↓</a><span>3개 장 · {len(slides)}개 슬라이드</span></div><div class="hero-formula" aria-label="포트폴리오 분산">$$\\sigma_p^2=\\mathbf{{w}}^\\top\\Sigma\\mathbf{{w}}$$</div></section>
<section class="learning-path"><div class="section-kicker">학습 경로</div><h2>한 흐름으로 연결되는 세 장</h2><div class="path-line"><span>자산의 현금흐름</span><b>→</b><span>수익률과 위험</span><b>→</b><span>분산투자</span><b>→</b><span>효율적 선택</span></div><div class="overview-grid">{''.join(cards)}</div></section>
<section class="home-note"><h2>읽는 방법</h2><p>왼쪽에서 슬라이드 화면을 확인하고 오른쪽 해설에서 개념의 배경, 계산 과정, 경제학적 의미를 따라가세요. 이미지를 눌러 확대할 수 있습니다. 추가 설명은 필요한 곳에서 펼쳐 읽을 수 있습니다.</p><details class="further-reading"><summary>더 읽을 자료</summary><ul>{refs}</ul></details></section>{footer('')}</main>'''
    return layout('', '전체 목차', '투자와 금융자산, 수익률과 위험, 두 자산 포트폴리오를 66개 슬라이드에 따라 배우는 학습 가이드.', content)


def lecture(chapter: dict, slides: list[dict], chapter_index: int) -> str:
    number = chapter['number']
    chapter_links = []
    for other in CHAPTERS:
        count = sum(s['chapter'] == other['slug'] for s in slides)
        current = ' is-current' if other['slug'] == chapter['slug'] else ''
        chapter_links.append(f'''<a class="chapter-link{current}" href="{other['number']}.html"><span class="chapter-num">{other['number']}</span><span><strong>{e(other['title'])}</strong><small>{e(other['tagline'])}</small></span><span class="chapter-count">{count}</span></a>''')
    own = [s for s in slides if s['chapter'] == chapter['slug']]
    slide_links = ''.join(f'<a href="#s{s["page"]:02}" data-slide-link="{s["page"]:02}"><span>{s["page"]:02}</span>{e(s["title"])}</a>' for s in own)
    sections = []
    for s in own:
        slide_number = f'{s["page"]:02}'
        src = '../' + s['image']
        case = s['case']
        case_html = f'<details class="case-note"><summary>{e(case["title"])}</summary>{case["html"]}</details>'
        supplement = s.get('supplement')
        supplement_html = f'<details><summary>{e(supplement["title"])}</summary>{supplement["html"]}</details>' if supplement else ''
        lab = '<div id="portfolio-lab"></div>' if s['id'] == '03-two-assets/18' else ''
        sections.append(f'''<section class="slide" id="s{slide_number}" data-slide="{slide_number}"><div class="slide-heading"><span class="slide-index">{number} / {slide_number}</span><h2>{e(s['title'])}</h2></div><div class="slide-grid"><figure class="slide-figure"><button type="button" class="slide-image-button" data-zoom-src="{e(src)}" data-zoom-label="{e(chapter['title'])} · 슬라이드 {slide_number}" aria-label="슬라이드 {slide_number} 이미지 확대"><img src="{e(src)}" alt="{e(chapter['title'])} 슬라이드 {slide_number}: {e(s['title'])}" width="1600" height="1200" loading="lazy" decoding="async"><span class="zoom-hint">확대해서 보기 ↗</span></button><figcaption>슬라이드 {slide_number}</figcaption></figure><div class="explanation">{s['html']}{case_html}{supplement_html}{lab}</div></div></section>''')
    prev = CHAPTERS[chapter_index - 1] if chapter_index else None
    next_ = CHAPTERS[chapter_index + 1] if chapter_index + 1 < len(CHAPTERS) else None
    pager = f'<a href="{prev["number"]}.html"><small>이전 장</small><strong>← {e(prev["title"])}</strong></a>' if prev else '<span></span>'
    pager += f'<a href="{next_["number"]}.html"><small>다음 장</small><strong>{e(next_["title"])} →</strong></a>' if next_ else '<span></span>'
    content = f'''<div class="layout"><aside class="sidebar"><a class="sidebar-home" href="../index.html">← 전체 목차</a><div class="sidebar-label">강의</div><nav aria-label="강의 목록" class="chapter-nav">{''.join(chapter_links)}</nav><div class="sidebar-label sidebar-label-slides">이 장의 슬라이드</div><nav aria-label="슬라이드 목차" class="slide-nav">{slide_links}</nav></aside><main id="main" class="lecture-main"><section class="lecture-hero"><div class="eyebrow">CHAPTER {number} · {len(own)} SLIDES</div><h1>{e(chapter['title'])}</h1><div class="lecture-intro"><p>{e(chapter['intro'])}</p></div><div class="lecture-start"><a href="#s01">첫 슬라이드로 내려가기 ↓</a><span>{chapter_index + 1} / {len(CHAPTERS)}</span></div></section>{''.join(sections)}<nav class="chapter-pager" aria-label="이전·다음 장">{pager}</nav>{footer('../')}</main></div>'''
    return layout('../', chapter['title'], f'{chapter["title"]}: {chapter["intro"]}', content)


def build_site(root: Path, slides: list[dict]) -> None:
    data = [{k: (v.replace(r'\boldsymbol', r'\mathbf') if k == 'html' else v) for k, v in slide.items() if k not in ('raw', 'case', 'supplement')} | {'case': {'title': slide['case']['title'], 'html': slide['case']['html'].replace(r'\boldsymbol', r'\mathbf')}} | ({'supplement': {'title': slide['supplement']['title'], 'html': slide['supplement']['html'].replace(r'\boldsymbol', r'\mathbf')}} if slide.get('supplement') else {}) for slide in slides]
    (root / 'data.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    (root / 'index.html').write_text(home(data), encoding='utf-8')
    lecture_dir = root / 'lecture'
    lecture_dir.mkdir(exist_ok=True)
    for i, chapter in enumerate(CHAPTERS):
        (lecture_dir / f'{chapter["number"]}.html').write_text(lecture(chapter, data, i), encoding='utf-8')
