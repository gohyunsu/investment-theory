const state = { slides: [], selected: 0, query: '' };
const $ = id => document.getElementById(id);
const chapters = [
  ['01-intro', '1부 · 투자와 금융자산', '투자의 구조'],
  ['02-risk-return', '2부 · 수익률과 위험', '불확실성의 측정'],
  ['03-two-assets', '3부 · 두 자산 포트폴리오', '분산과 최적화']
];

function normalize(text) { return (text || '').toLocaleLowerCase('ko').replace(/\s+/g, ' '); }
function textFromHtml(html) { const box = document.createElement('div'); box.innerHTML = html; return box.textContent || ''; }
function currentFromHash() { const id = decodeURIComponent(location.hash.slice(1)); const i = state.slides.findIndex(s => s.id === id); return i < 0 ? 0 : i; }
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

function renderNav() {
  const query = normalize(state.query);
  $('nav').innerHTML = chapters.map(([slug, name]) => {
    const items = state.slides.filter(s => s.chapter === slug && (!query || normalize(s.title + ' ' + textFromHtml(s.html)).includes(query)));
    if (!items.length) return '';
    return `<div class="chapter"><div class="chapter-head">${escapeHtml(name)}</div>${items.map(s => `<a href="#${s.id}" class="${state.slides[state.selected].id === s.id ? 'active' : ''}" ${state.slides[state.selected].id === s.id ? 'aria-current="page"' : ''}><span class="n">${String(s.page).padStart(2,'0')}</span><span>${escapeHtml(s.title)}</span></a>`).join('')}</div>`;
  }).join('') || '<p class="chapter-head">검색 결과가 없습니다.</p>';
  $('nav').querySelector('a.active')?.scrollIntoView({block:'nearest'});
}

function portfolioLab() {
  return `<section class="lab" aria-label="분산투자 실험실"><h3>상관관계를 바꾸면 프런티어가 어떻게 움직일까?</h3><p>두 자산의 기대수익은 10%와 14%, 표준편차는 15%와 20%로 고정했다. 상관계수와 첫 자산의 비중을 움직여 위험이 어떻게 바뀌는지 확인해 보자.</p><div class="lab-controls"><label>상관계수 <strong id="rho-value"></strong> <input id="rho" type="range" min="-100" max="100" value="20" aria-label="상관계수"></label><label>자산 1 비중 <strong id="weight-value"></strong> <input id="weight" type="range" min="0" max="100" value="60" aria-label="자산 1 비중"></label></div><svg id="portfolio-plot" viewBox="0 0 620 340" role="img" aria-label="선택한 상관계수에서 두 자산의 기대수익과 표준편차 관계"></svg><div class="lab-metrics"><span id="lab-mean"></span><span id="lab-risk"></span><span id="lab-gmv"></span></div></section>`;
}

function drawLab() {
  const rho = Number($('rho').value) / 100, w = Number($('weight').value) / 100;
  const risk = x => Math.sqrt(.15**2*x*x + .20**2*(1-x)**2 + 2*x*(1-x)*rho*.15*.20);
  const mean = x => .10*x + .14*(1-x);
  const xCoord = x => 54 + x / .25 * 490, yCoord = y => 280 - (y - .08) / .07 * 215;
  const coordinates = Array.from({length:101}, (_,i) => `${i?'L':'M'} ${xCoord(risk(i/100)).toFixed(1)} ${yCoord(mean(i/100)).toFixed(1)}`).join(' ');
  const a = .15**2 + .20**2 - 2*rho*.15*.20;
  const gmv = Math.max(0, Math.min(1, (.20**2-rho*.15*.20)/a));
  $('rho-value').textContent = rho.toFixed(2);
  $('weight-value').textContent = `${Math.round(w*100)}%`;
  $('lab-mean').textContent = `기대수익 ${(mean(w)*100).toFixed(2)}%`;
  $('lab-risk').textContent = `표준편차 ${(risk(w)*100).toFixed(2)}%`;
  $('lab-gmv').textContent = `최소분산 비중 ${(gmv*100).toFixed(1)}%`;
  $('portfolio-plot').innerHTML = `<path d="M 54 42 L 54 280 L 553 280" fill="none" stroke="#a9bcbc" stroke-width="1.5"/><path d="${coordinates}" fill="none" stroke="#277d73" stroke-width="3"/><circle cx="${xCoord(risk(w))}" cy="${yCoord(mean(w))}" r="7" fill="#bd704b" stroke="white" stroke-width="2"/><circle cx="${xCoord(risk(gmv))}" cy="${yCoord(mean(gmv))}" r="5" fill="#122d46"/><text x="53" y="310" font-size="12" fill="#687d80">0</text><text x="497" y="310" font-size="12" fill="#687d80">25% 변동성</text><text x="7" y="47" font-size="12" fill="#687d80">15%</text><text x="7" y="281" font-size="12" fill="#687d80">8%</text><text x="64" y="33" font-size="12" fill="#687d80">기대수익</text>`;
}

function renderSlide(scroll = true) {
  state.selected = currentFromHash();
  const slide = state.slides[state.selected];
  const chapter = chapters.find(c => c[0] === slide.chapter);
  $('reader').innerHTML = `<div class="chapter-banner"><div class="kicker">${escapeHtml(chapter[1])}</div><h2>${escapeHtml(chapter[2])}</h2><p>개념 · 계산 · 경제학적 직관을 한 흐름으로 읽기</p></div><div class="slide-heading"><div><div class="number">${escapeHtml(chapter[1])} / ${String(slide.page).padStart(2,'0')}</div><h2>${escapeHtml(slide.title)}</h2></div><div class="count">${String(state.selected+1).padStart(2,'0')} / 66</div></div><div class="slide-grid"><div class="source-panel"><div class="source-label"><span>SLIDE ${String(slide.page).padStart(2,'0')}</span><span>${escapeHtml(chapter[1])}</span></div><a class="slide-image" href="${slide.image}" target="_blank" aria-label="슬라이드 ${slide.page} 이미지 크게 보기"><img src="${slide.image}" width="1600" alt="${escapeHtml(slide.title)} 슬라이드" decoding="async"></a><div class="hint">이미지를 누르면 크게 볼 수 있습니다.</div></div><article class="reading"><h3>개념과 해설</h3>${slide.html}${slide.supplement ? `<details><summary>${escapeHtml(slide.supplement.title)}</summary>${slide.supplement.html}</details>` : ''}${slide.id === '03-two-assets/18' ? portfolioLab() : ''}</article></div>`;
  $('previous').disabled = state.selected === 0;
  $('next').disabled = state.selected === state.slides.length - 1;
  $('position').textContent = `${state.selected + 1} / ${state.slides.length}`;
  $('progress-fill').style.width = `${(state.selected+1)/state.slides.length*100}%`;
  renderNav();
  if (slide.id === '03-two-assets/18') { $('rho').addEventListener('input', drawLab); $('weight').addEventListener('input', drawLab); drawLab(); }
  if (window.MathJax?.typesetPromise) MathJax.typesetPromise([$('reader')]).catch(error => console.error(error));
  if (scroll) window.scrollTo({top:0,behavior:'instant'});
}

async function start() {
  try {
    const response = await fetch('data.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.slides = await response.json();
    if (state.slides.length !== 66) throw new Error('슬라이드 데이터가 완전하지 않습니다.');
    renderSlide(false);
    addEventListener('hashchange', () => renderSlide());
    $('search').addEventListener('input', event => { state.query = event.target.value; renderNav(); });
    $('previous').addEventListener('click', () => { if (state.selected > 0) location.hash = state.slides[state.selected-1].id; });
    $('next').addEventListener('click', () => { if (state.selected < state.slides.length-1) location.hash = state.slides[state.selected+1].id; });
    addEventListener('keydown', event => { if (event.target.matches('input,button,summary') || $('references').open) return; if (event.key === 'ArrowLeft' && state.selected > 0) location.hash = state.slides[state.selected-1].id; if (event.key === 'ArrowRight' && state.selected < state.slides.length-1) location.hash = state.slides[state.selected+1].id; });
    $('refs-open').addEventListener('click', () => $('references').showModal());
    $('refs-close').addEventListener('click', () => $('references').close());
  } catch (error) { $('reader').innerHTML = `<p>가이드를 불러오지 못했습니다: ${escapeHtml(error.message)}</p>`; }
}
start();
