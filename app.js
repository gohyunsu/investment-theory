const prefix = document.body.dataset.prefix || '';
const chapterNumbers = {'01-intro':'01','02-risk-return':'02','03-two-assets':'03'};
const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

// Preserve bookmarks from the earlier slide-at-a-time site.
if (!prefix && location.hash) {
  const old = /^#(01-intro|02-risk-return|03-two-assets)\/(\d+)$/.exec(decodeURIComponent(location.hash));
  if (old) location.replace(`lecture/${chapterNumbers[old[1]]}.html#s${old[2].padStart(2, '0')}`);
}

const searchDialog = document.getElementById('search-dialog');
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
let slideData;
let loading;
function getSlides() {
  if (!loading) loading = fetch(`${prefix}data.json`).then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }).then(data => {
    const parser = document.createElement('div');
    slideData = data.map(slide => {
      parser.innerHTML = slide.html + (slide.case?.html || '') + (slide.supplement?.html || '');
      return {...slide, text: parser.textContent.replace(/\s+/g, ' ')};
    });
    return slideData;
  });
  return loading;
}
function renderSearch(query) {
  const words = query.trim().toLocaleLowerCase('ko').split(/\s+/).filter(Boolean);
  if (!words.length) { searchResults.innerHTML = '<p>찾고 싶은 개념이나 사례를 입력하세요.</p>'; return; }
  const found = (slideData || []).filter(slide => words.every(word => `${slide.title} ${slide.chapterName} ${slide.text}`.toLocaleLowerCase('ko').includes(word))).slice(0, 20);
  searchResults.innerHTML = found.length ? found.map(slide => {
    const n = chapterNumbers[slide.chapter];
    return `<a href="${prefix}lecture/${n}.html#s${String(slide.page).padStart(2, '0')}"><small>${n}장 · 슬라이드 ${String(slide.page).padStart(2, '0')}</small><strong>${escapeHtml(slide.title)}</strong><span>${escapeHtml(slide.text.slice(0, 130))}…</span></a>`;
  }).join('') : '<p>일치하는 슬라이드가 없습니다.</p>';
}
async function openSearch() {
  if (!searchDialog.open) searchDialog.showModal();
  searchInput.focus();
  searchResults.innerHTML = '<p>검색 내용을 준비하는 중입니다.</p>';
  try { await getSlides(); renderSearch(searchInput.value); }
  catch { searchResults.innerHTML = '<p>검색 내용을 불러오지 못했습니다.</p>'; }
}
document.querySelectorAll('[data-search-trigger]').forEach(button => button.addEventListener('click', openSearch));
document.querySelectorAll('[data-search-close]').forEach(button => button.addEventListener('click', () => searchDialog.close()));
searchInput.addEventListener('input', () => renderSearch(searchInput.value));
searchResults.addEventListener('click', event => { if (event.target.closest('a')) searchDialog.close(); });
searchDialog.addEventListener('click', event => { if (event.target === searchDialog) searchDialog.close(); });
document.addEventListener('keydown', event => {
  if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)) { event.preventDefault(); openSearch(); }
});

const slideDialog = document.getElementById('slide-dialog');
document.querySelectorAll('[data-zoom-src]').forEach(button => button.addEventListener('click', () => {
  const img = slideDialog.querySelector('img');
  img.src = button.dataset.zoomSrc;
  img.alt = button.dataset.zoomLabel;
  slideDialog.querySelector('p').textContent = button.dataset.zoomLabel;
  slideDialog.showModal();
}));
document.querySelectorAll('[data-dialog-close]').forEach(button => button.addEventListener('click', () => slideDialog.close()));
slideDialog.addEventListener('click', event => { if (event.target === slideDialog) slideDialog.close(); });

const sections = [...document.querySelectorAll('.slide')];
const slideLinks = [...document.querySelectorAll('[data-slide-link]')];
if (sections.length && slideLinks.length) {
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (visible.length) slideLinks.forEach(link => link.classList.toggle('is-active', link.dataset.slideLink === visible[0].target.dataset.slide));
  }, {rootMargin:'-90px 0px -65% 0px'});
  sections.forEach(section => observer.observe(section));
}
const progress = document.querySelector('.reading-progress');
function updateProgress() {
  const maximum = document.documentElement.scrollHeight - innerHeight;
  progress.style.width = `${maximum > 0 ? Math.max(0, Math.min(100, scrollY / maximum * 100)) : 0}%`;
}
addEventListener('scroll', updateProgress, {passive:true});
addEventListener('resize', updateProgress);
updateProgress();

// Math typesetting changes section heights; settle direct slide links afterwards.
if (/^#s\d{2}$/.test(location.hash)) {
  const target = document.getElementById(location.hash.slice(1));
  const alignTarget = () => requestAnimationFrame(() => target?.scrollIntoView({block:'start', behavior:'instant'}));
  addEventListener('load', alignTarget, {once:true});
  if (window.MathJax?.startup?.promise) MathJax.startup.promise.then(alignTarget).catch(() => {});
}

function portfolioLab() {
  return `<section class="lab" aria-label="분산투자 실험실"><h3>상관관계를 바꾸면 프런티어가 어떻게 움직일까?</h3><p>두 자산의 기대수익은 10%와 14%, 표준편차는 15%와 20%로 고정했다. 상관계수와 첫 자산의 비중을 움직여 위험이 어떻게 바뀌는지 확인해 보자.</p><div class="lab-controls"><label>상관계수 <strong id="rho-value"></strong> <input id="rho" type="range" min="-100" max="100" value="20" aria-label="상관계수"></label><label>자산 1 비중 <strong id="weight-value"></strong> <input id="weight" type="range" min="0" max="100" value="60" aria-label="자산 1 비중"></label></div><svg id="portfolio-plot" viewBox="0 0 620 340" role="img" aria-label="선택한 상관계수에서 두 자산의 기대수익과 표준편차 관계"></svg><div class="lab-metrics"><span id="lab-mean"></span><span id="lab-risk"></span><span id="lab-gmv"></span></div></section>`;
}
const labSlot = document.getElementById('portfolio-lab');
if (labSlot) {
  labSlot.innerHTML = portfolioLab();
  const $ = id => document.getElementById(id);
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
    $('portfolio-plot').innerHTML = `<path d="M 54 42 L 54 280 L 553 280" fill="none" stroke="#a9bcbc" stroke-width="1.5"/><path d="${coordinates}" fill="none" stroke="#146d70" stroke-width="3"/><circle cx="${xCoord(risk(w))}" cy="${yCoord(mean(w))}" r="7" fill="#b46e29" stroke="white" stroke-width="2"/><circle cx="${xCoord(risk(gmv))}" cy="${yCoord(mean(gmv))}" r="5" fill="#17243a"/><text x="53" y="310" font-size="12" fill="#687d80">0</text><text x="497" y="310" font-size="12" fill="#687d80">25% 변동성</text><text x="7" y="47" font-size="12" fill="#687d80">15%</text><text x="7" y="281" font-size="12" fill="#687d80">8%</text><text x="64" y="33" font-size="12" fill="#687d80">기대수익</text>`;
  }
  $('rho').addEventListener('input', drawLab);
  $('weight').addEventListener('input', drawLab);
  drawLab();
}
