# 금융투자 이론 학습 가이드

투자와 금융자산, 수익률과 위험, 두 자산 포트폴리오를 66개의 순서 있는 장면으로 읽는 한국어 학습 가이드입니다. 각 장면은 화면 자료와 개념 설명을 나란히 제시하며, 수식은 가정에서 계산과 경제학적 해석까지 이어집니다.

## 읽는 순서

1. **투자의 구조** — 실물·금융자산, 주식·채권·파생상품, 투자관리 과정.
2. **불확실성의 측정** — 보유기간 수익률, 모멘트, 표본 추정, VaR, 공분산.
3. **분산과 최적화** — 자본배분선, 샤프비율, 최소분산과 접점 포트폴리오.

웹 가이드에서는 검색으로 개념을 찾고, 슬라이드 이미지를 확대하고, 상관계수를 바꾸며 포트폴리오의 위험을 탐색할 수 있습니다. 16개 보충 설명은 해당 장면에서 펼쳐 읽을 수 있습니다. [PDF 가이드](guide.pdf)와 [LaTeX 원고](guide.tex)에는 같은 본문과 보충 설명이 순서대로 담겨 있습니다.

## 핵심 계산

- 보유기간 수익률: $R_t=(P_t-P_{t-1}+D_t)/P_{t-1}$.
- 두 자산 분산: $\sigma_p^2=w^2\sigma_1^2+(1-w)^2\sigma_2^2+2w(1-w)\sigma_{12}$.
- 최소분산 비중: $w_{\mathrm{GMV}}=(\sigma_2^2-\sigma_{12})/(\sigma_1^2+\sigma_2^2-2\sigma_{12})$.
- 접점 비중: $\boldsymbol w_T=\Sigma^{-1}(\boldsymbol\mu-r_f\boldsymbol1)/(\boldsymbol1^\top\Sigma^{-1}(\boldsymbol\mu-r_f\boldsymbol1))$.

## 프로젝트 구성

| 경로 | 역할 |
| --- | --- |
| `content/01-intro.md` 등 | 3개 장, 66개 장면의 본문 |
| `content/supplements.md` | 펼쳐 읽는 심화 설명 |
| `assets/slides/` | 장면별 웹 이미지 |
| `tools/build.py` | 단일 원고에서 사이트 데이터와 LaTeX 문서 생성 |
| `app.js`, `style.css`, `index.html` | 정적 웹 가이드 |
| `guide.tex` | 독립 실행형 LaTeX 문서 |
| `guide.pdf` | 컴파일된 가이드 |
| `docs/` | 계산 검증과 편집 구조 |

`python tools/build.py`로 사이트 데이터와 TeX 문서를 다시 생성할 수 있습니다. XeLaTeX와 한국어 글꼴이 있는 환경에서는 `python tools/build_pdf.py`로 PDF까지 다시 만들 수 있습니다. 새 장면의 화면 자료는 `python tools/render_slides.py <로컬 PDF 디렉터리>`로 변환할 수 있습니다. 사이트는 정적 파일이므로 로컬에서는 `python -m http.server 8123`으로 확인할 수 있습니다.

## 더 읽을 자료

- [SEC Investor.gov — 자산배분과 분산투자](https://www.investor.gov/introduction-investing/getting-started/asset-allocation)
- [SEC Investor.gov — 투자 위험](https://www.investor.gov/introduction-investing/investing-basics/what-risk)
- [미국 재무부 — 국채 가격과 금리](https://www.treasurydirect.gov/marketable-securities/understanding-pricing/)
- [FINRA — 증거금 거래](https://www.finra.org/investors/investing/investment-products/stocks)
- [한국거래소 — 코스피200 선물](https://global.krx.co.kr/contents/GLB/02/0201/0201040201/GLB0201040201.jsp)
- [Harry Markowitz, *Portfolio Selection* (1952)](https://doi.org/10.1111/j.1540-6261.1952.tb01525.x)
- [미국 연방준비제도 — 위험 프리미엄](https://www.federalreserve.gov/publications/may-2021-asset-valuations.htm)

이 자료의 예시는 개념 설명을 위한 것이며 수익률 예측이나 투자 권유가 아닙니다.
