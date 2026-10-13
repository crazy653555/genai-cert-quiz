# -*- coding: utf-8 -*-
import sqlite3, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(ROOT, "複習測驗網站")
DB_PATH = os.path.join(SITE_DIR, "quiz.db")
OUT_PATH = os.path.join(SITE_DIR, "index.html")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("""
    SELECT id, source, topic, question, option_a, option_b, option_c, option_d,
           correct_option, explanation, has_caveat, caveat_note
    FROM questions ORDER BY id
""")
rows = [dict(r) for r in cur.fetchall()]
conn.close()

data_json = json.dumps(rows, ensure_ascii=False)

template = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>生成式AI認證 隨機複習測驗</title>
<style>
  :root {
    --bg: #f4f6fb;
    --card-bg: #ffffff;
    --text: #1b2430;
    --muted: #6b7686;
    --border: #e3e7ef;
    --accent: #3b5bdb;
    --accent-weak: #eef1fd;
    --correct: #2f9e44;
    --correct-weak: #ebfbee;
    --wrong: #e03131;
    --wrong-weak: #fff0f0;
    --warn: #e8590c;
    --warn-weak: #fff4e6;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #14171f; --card-bg: #1c2029; --text: #e7eaf1; --muted: #9aa3b2;
      --border: #2b3040; --accent: #7c93ff; --accent-weak: #232a43;
      --correct: #51cf66; --correct-weak: #14301c;
      --wrong: #ff6b6b; --wrong-weak: #351414;
      --warn: #ffa94d; --warn-weak: #332107;
    }
  }
  :root[data-theme="dark"] {
    --bg: #14171f; --card-bg: #1c2029; --text: #e7eaf1; --muted: #9aa3b2;
    --border: #2b3040; --accent: #7c93ff; --accent-weak: #232a43;
    --correct: #51cf66; --correct-weak: #14301c;
    --wrong: #ff6b6b; --wrong-weak: #351414;
    --warn: #ffa94d; --warn-weak: #332107;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font-family: "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", system-ui, sans-serif;
    line-height: 1.6;
  }
  .wrap { max-width: 720px; margin: 0 auto; padding: 20px 16px 60px; }
  @media (min-width: 900px) {
    .wrap { max-width: 760px; padding-top: 32px; }
  }
  header { display: flex; align-items: baseline; justify-content: space-between; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
  h1 { font-size: 1.25rem; margin: 0; }
  h2 { font-size: 1rem; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 0.8125rem; }

  .card {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 14px; padding: 20px;
  }
  .card + .card { margin-top: 16px; }

  fieldset { border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; margin: 0 0 16px; }
  legend { font-size: 0.8125rem; color: var(--muted); padding: 0 6px; }
  .src-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; }
  label.chk {
    display: flex; align-items: center; gap: 8px; font-size: 0.875rem;
    padding: 8px; border-radius: 8px; cursor: pointer; min-height: 40px;
  }
  label.chk:hover { background: var(--accent-weak); }
  .toggle-row { display: flex; align-items: center; gap: 8px; font-size: 0.875rem; margin-bottom: 10px; min-height: 32px; }
  input[type="checkbox"] { width: 18px; height: 18px; flex: none; }
  input[type="number"] { min-height: 36px; }

  button {
    font-size: 0.875rem; border-radius: 8px; border: 1px solid var(--border);
    background: var(--card-bg); color: var(--text); padding: 10px 16px; cursor: pointer;
    min-height: 44px; touch-action: manipulation;
  }
  button.primary { background: var(--accent); border-color: var(--accent); color: #fff; font-weight: 600; width: 100%; padding: 12px; font-size: 0.9375rem; }
  button.secondary { width: 100%; margin-top: 10px; }
  button:disabled { opacity: .5; cursor: default; }

  .progress-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.8125rem; color: var(--muted); margin-bottom: 14px; flex-wrap: wrap; gap: 8px; }
  .progress-row b { color: var(--text); }
  .bar-track { height: 6px; border-radius: 999px; background: var(--border); overflow: hidden; margin-bottom: 16px; }
  .bar-fill { height: 100%; background: var(--accent); transition: width .2s; }

  .meta { display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: var(--muted); margin-bottom: 10px; gap: 8px; flex-wrap: wrap; }
  .tag { display: inline-block; background: var(--accent-weak); color: var(--accent); border-radius: 999px; padding: 2px 10px; font-size: 0.75rem; }
  .question { font-size: 1.0625rem; font-weight: 600; margin: 0 0 16px; white-space: pre-wrap; }
  .options { display: flex; flex-direction: column; gap: 10px; }
  .option {
    display: flex; gap: 10px; align-items: flex-start; text-align: left;
    padding: 14px; border: 1px solid var(--border); border-radius: 10px;
    background: var(--bg); color: var(--text); font-size: 0.9375rem; cursor: pointer;
    transition: border-color .15s, background .15s; width: 100%;
    min-height: 48px; touch-action: manipulation;
  }
  .option:hover:not(:disabled) { border-color: var(--accent); }
  .option .letter {
    flex: none; width: 1.6em; height: 1.6em; border-radius: 50%;
    border: 1px solid var(--border); display: flex; align-items: center; justify-content: center;
    font-size: 0.8125rem; font-weight: 700; color: var(--muted);
  }
  .option.correct { border-color: var(--correct); background: var(--correct-weak); }
  .option.correct .letter { border-color: var(--correct); color: var(--correct); }
  .option.wrong { border-color: var(--wrong); background: var(--wrong-weak); }
  .option.wrong .letter { border-color: var(--wrong); color: var(--wrong); }
  .option:disabled { cursor: default; }

  .result-box { margin-top: 16px; }
  .result-banner { font-weight: 700; font-size: 0.9375rem; margin-bottom: 8px; }
  .result-banner.correct { color: var(--correct); }
  .result-banner.wrong { color: var(--wrong); }
  .explanation {
    font-size: 0.875rem; color: var(--text); background: var(--bg);
    border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; white-space: pre-wrap;
  }
  .caveat {
    margin-top: 10px; font-size: 0.8125rem; color: var(--warn); background: var(--warn-weak);
    border: 1px solid var(--warn); border-radius: 10px; padding: 10px 14px; white-space: pre-wrap;
  }
  .next-row { margin-top: 18px; }

  .summary-stat { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 0.9375rem; }
  .summary-stat:last-child { border-bottom: none; }
  .big-accuracy { font-size: 2.5rem; font-weight: 800; color: var(--accent); text-align: center; margin: 6px 0 2px; }

  .review-item {
    border: 1px solid var(--border); border-radius: 10px; padding: 14px; margin-bottom: 12px;
  }
  .review-item .meta { margin-bottom: 8px; }
  .review-item .question { font-size: 0.9375rem; margin-bottom: 10px; }
  .review-line { font-size: 0.875rem; margin: 4px 0; }
  .review-line .your-ans { color: var(--wrong); font-weight: 600; }
  .review-line .correct-ans { color: var(--correct); font-weight: 600; }
  .review-explanation { font-size: 0.8125rem; color: var(--muted); margin-top: 8px; white-space: pre-wrap; }
  .no-wrong { text-align: center; color: var(--muted); padding: 20px 0; }

  .font-ctrl { display: flex; align-items: center; gap: 4px; }
  .font-ctrl button { min-height: 36px; min-width: 40px; padding: 4px 10px; font-weight: 700; }
  .font-ctrl .font-val { font-size: 0.8125rem; color: var(--muted); min-width: 3em; text-align: center; }

  footer { margin-top: 24px; font-size: 0.75rem; color: var(--muted); text-align: center; }
  .hidden { display: none !important; }

  @media (max-width: 400px) {
    .card { padding: 16px; }
    .question { font-size: 1rem; }
    h1 { font-size: 1.125rem; }
    .big-accuracy { font-size: 2.125rem; }
  }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <h1>生成式AI能力認證 複習測驗</h1>
      <div class="sub">題庫共 <span id="totalAll">0</span> 題</div>
    </div>
    <div class="font-ctrl" role="group" aria-label="字體大小">
      <button type="button" id="fontDownBtn" aria-label="縮小字體">A−</button>
      <span class="font-val" id="fontVal">100%</span>
      <button type="button" id="fontUpBtn" aria-label="放大字體">A＋</button>
    </div>
  </header>

  <!-- ===== Setup screen ===== -->
  <div class="card" id="setupScreen">
    <h2>開始前先設定</h2>
    <p class="sub" style="margin-top:0;">選好來源與選項設定後開始，題目會隨機排序且不重複，直到該範圍內題目全部出完。</p>

    <fieldset>
      <legend>考試來源（可複選）</legend>
      <div class="src-grid" id="sourceGrid"></div>
    </fieldset>

    <div class="toggle-row">
      <input type="checkbox" id="randomizeOptions" checked>
      <label for="randomizeOptions">選項隨機排序（關閉則維持 A/B/C/D 原始順序）</label>
    </div>
    <div class="toggle-row">
      <input type="checkbox" id="excludeCaveat">
      <label for="excludeCaveat">排除有 ⚠️ 爭議備註的題目</label>
    </div>

    <div class="toggle-row" style="flex-wrap:wrap;">
      <input type="checkbox" id="limitEnabled">
      <label for="limitEnabled">限制本次出題數（隨機抽選，不重複）：</label>
      <input type="number" id="limitCount" min="1" value="80" style="width:80px; padding:6px 8px; border-radius:8px; border:1px solid var(--border); background:var(--card-bg); color:var(--text);" disabled>
      <span class="sub">題</span>
    </div>

    <p class="sub">本次範圍共 <b id="poolCount">0</b> 題，實際出題 <b id="effectiveCount">0</b> 題</p>
    <button class="primary" id="startBtn">開始測驗</button>
  </div>

  <!-- ===== Quiz screen ===== -->
  <div id="quizScreen" class="hidden">
    <div class="progress-row">
      <span>進度：<b id="progressText">0 / 0</b></span>
      <span>答對：<b id="correctCount">0</b>　正確率：<b id="accuracy">0%</b></span>
    </div>
    <div class="bar-track"><div class="bar-fill" id="progressBar" style="width:0%"></div></div>

    <div class="card">
      <div class="meta">
        <span class="tag" id="currentSource"></span>
        <span class="tag" id="currentTopic"></span>
        <span id="currentId"></span>
      </div>
      <p class="question" id="questionText"></p>
      <div class="options" id="optionsBox"></div>

      <div class="result-box hidden" id="resultBox">
        <div class="result-banner" id="resultBanner"></div>
        <div class="explanation" id="explanationText"></div>
        <div class="caveat hidden" id="caveatText"></div>
      </div>

      <div class="next-row">
        <button class="primary" id="nextBtn" disabled>下一題</button>
      </div>
    </div>
    <button class="secondary" id="backToSetupBtn">結束測驗並看結果</button>
  </div>

  <!-- ===== Summary screen ===== -->
  <div id="summaryScreen" class="hidden">
    <div class="card">
      <h2>測驗結束</h2>
      <div class="big-accuracy" id="summaryAccuracy">0%</div>
      <div class="summary-stat"><span>已作答</span><b id="summaryTotal">0</b></div>
      <div class="summary-stat"><span>答對</span><b id="summaryCorrect">0</b></div>
      <div class="summary-stat"><span>答錯</span><b id="summaryWrong">0</b></div>
      <button class="primary" id="restartSameBtn" style="margin-top:16px;">用同樣設定再測一次</button>
      <button class="secondary" id="backSetupFromSummaryBtn">重新選擇設定</button>
    </div>

    <div class="card" id="reviewCard">
      <h2>答錯題目重新整理</h2>
      <div id="reviewList"></div>
    </div>
  </div>

  <footer>資料來源：資策會生成式AI能力認證解題影片／AI白話拆解×認證實戰通關密笈 整理（含人工重建與勘誤備註，應試前請以官方題庫為準）</footer>
</div>

<script>
const QUESTIONS = __DATA_JSON__;

const sourceGridEl = document.getElementById('sourceGrid');
const totalAllEl = document.getElementById('totalAll');
const poolCountEl = document.getElementById('poolCount');
const randomizeOptionsEl = document.getElementById('randomizeOptions');
const excludeCaveatEl = document.getElementById('excludeCaveat');
const limitEnabledEl = document.getElementById('limitEnabled');
const limitCountEl = document.getElementById('limitCount');
const effectiveCountEl = document.getElementById('effectiveCount');
const startBtn = document.getElementById('startBtn');

const setupScreen = document.getElementById('setupScreen');
const quizScreen = document.getElementById('quizScreen');
const summaryScreen = document.getElementById('summaryScreen');

const progressText = document.getElementById('progressText');
const progressBar = document.getElementById('progressBar');
const correctCountEl = document.getElementById('correctCount');
const accuracyEl = document.getElementById('accuracy');
const currentSourceEl = document.getElementById('currentSource');
const currentTopicEl = document.getElementById('currentTopic');
const currentIdEl = document.getElementById('currentId');
const questionTextEl = document.getElementById('questionText');
const optionsBoxEl = document.getElementById('optionsBox');
const resultBoxEl = document.getElementById('resultBox');
const resultBannerEl = document.getElementById('resultBanner');
const explanationTextEl = document.getElementById('explanationText');
const caveatTextEl = document.getElementById('caveatText');
const nextBtn = document.getElementById('nextBtn');
const backToSetupBtn = document.getElementById('backToSetupBtn');

const summaryAccuracyEl = document.getElementById('summaryAccuracy');
const summaryTotalEl = document.getElementById('summaryTotal');
const summaryCorrectEl = document.getElementById('summaryCorrect');
const summaryWrongEl = document.getElementById('summaryWrong');
const restartSameBtn = document.getElementById('restartSameBtn');
const backSetupFromSummaryBtn = document.getElementById('backSetupFromSummaryBtn');
const reviewListEl = document.getElementById('reviewList');

let queue = [];
let qIndex = 0;
let answered = 0;
let correctCount = 0;
let currentQ = null;
let currentShuffledOptions = null; // [{letter, text, isCorrect}]
let wrongList = [];
const DISPLAY_LETTERS = ['A', 'B', 'C', 'D']; // [{source, topic, id, question, yourAnswer, correctLetter, correctText, explanation, has_caveat, caveat_note}]

function shuffleArray(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function buildSourceCheckboxes() {
  const sources = [...new Set(QUESTIONS.map(q => q.source))].sort();
  sourceGridEl.innerHTML = sources.map(s => {
    const count = QUESTIONS.filter(q => q.source === s).length;
    const topics = [...new Set(QUESTIONS.filter(q => q.source === s).map(q => q.topic))].join('、');
    return `<label class="chk">
      <input type="checkbox" class="srcChk" value="${s}">
      ${s}（${count}題・${topics}）
    </label>`;
  }).join('');
  sourceGridEl.querySelectorAll('.srcChk').forEach(cb => cb.addEventListener('change', updatePoolCount));
}

function getSelectedSources() {
  return [...sourceGridEl.querySelectorAll('.srcChk:checked')].map(cb => cb.value);
}

function currentFilteredSet() {
  const selected = getSelectedSources();
  const excludeCaveat = excludeCaveatEl.checked;
  return QUESTIONS.filter(q => {
    if (!selected.includes(q.source)) return false;
    if (excludeCaveat && q.has_caveat) return false;
    return true;
  });
}

function getEffectiveCount(poolSize) {
  if (!limitEnabledEl.checked) return poolSize;
  const n = parseInt(limitCountEl.value, 10);
  if (!n || n < 1) return poolSize;
  return Math.min(n, poolSize);
}

function updatePoolCount() {
  const size = currentFilteredSet().length;
  poolCountEl.textContent = size;
  limitCountEl.max = size || 1;
  effectiveCountEl.textContent = getEffectiveCount(size);
  startBtn.disabled = size === 0;
}

function startQuiz() {
  const pool = currentFilteredSet();
  if (pool.length === 0) {
    alert('目前設定下沒有題目，請至少選一個來源。');
    return;
  }
  const effectiveCount = getEffectiveCount(pool.length);
  queue = shuffleArray(pool).slice(0, effectiveCount);
  qIndex = 0;
  answered = 0;
  correctCount = 0;
  wrongList = [];
  setupScreen.classList.add('hidden');
  summaryScreen.classList.add('hidden');
  quizScreen.classList.remove('hidden');
  showQuestion();
}

function updateProgressUI() {
  progressText.textContent = (qIndex) + ' / ' + queue.length;
  progressBar.style.width = (queue.length ? (qIndex / queue.length * 100) : 0) + '%';
  correctCountEl.textContent = correctCount;
  accuracyEl.textContent = answered ? Math.round(correctCount / answered * 100) + '%' : '0%';
}

function showQuestion() {
  if (qIndex >= queue.length) {
    showSummary();
    return;
  }
  window.scrollTo(0, 0);
  resultBoxEl.classList.add('hidden');
  nextBtn.disabled = true;
  currentQ = queue[qIndex];
  updateProgressUI();

  currentSourceEl.textContent = currentQ.source;
  currentTopicEl.textContent = currentQ.topic;
  currentIdEl.textContent = '第 ' + currentQ.id + ' 題';
  questionTextEl.textContent = currentQ.question;

  const rawOptions = [
    { letter: 'A', text: currentQ.option_a, isCorrect: currentQ.correct_option === 'A' },
    { letter: 'B', text: currentQ.option_b, isCorrect: currentQ.correct_option === 'B' },
    { letter: 'C', text: currentQ.option_c, isCorrect: currentQ.correct_option === 'C' },
    { letter: 'D', text: currentQ.option_d, isCorrect: currentQ.correct_option === 'D' },
  ];
  currentShuffledOptions = randomizeOptionsEl.checked ? shuffleArray(rawOptions) : rawOptions;

  optionsBoxEl.innerHTML = '';
  currentShuffledOptions.forEach((opt, i) => {
    const btn = document.createElement('button');
    btn.className = 'option';
    btn.innerHTML = `<span class="letter">${DISPLAY_LETTERS[i]}</span><span>${opt.text}</span>`;
    btn.addEventListener('click', () => selectAnswer(i, btn));
    optionsBoxEl.appendChild(btn);
  });
}

function selectAnswer(pickedIndex, btnEl) {
  const allBtns = optionsBoxEl.querySelectorAll('.option');
  allBtns.forEach(b => b.disabled = true);

  const picked = currentShuffledOptions[pickedIndex];
  const isCorrect = picked.isCorrect;
  const correctIndex = currentShuffledOptions.findIndex(o => o.isCorrect);
  const correctDisplayLetter = DISPLAY_LETTERS[correctIndex];
  answered++;
  if (isCorrect) {
    correctCount++;
  } else {
    const correctOpt = currentShuffledOptions[correctIndex];
    wrongList.push({
      source: currentQ.source,
      topic: currentQ.topic,
      id: currentQ.id,
      question: currentQ.question,
      yourAnswer: picked.text,
      correctLetter: correctDisplayLetter,
      correctText: correctOpt.text,
      explanation: currentQ.explanation,
      has_caveat: currentQ.has_caveat,
      caveat_note: currentQ.caveat_note,
    });
  }

  allBtns.forEach((b, i) => {
    if (currentShuffledOptions[i].isCorrect) b.classList.add('correct');
    else if (i === pickedIndex) b.classList.add('wrong');
  });

  resultBannerEl.textContent = isCorrect ? '✓ 答對了！' : ('✗ 答錯了，正確答案是 ' + correctDisplayLetter);
  resultBannerEl.className = 'result-banner ' + (isCorrect ? 'correct' : 'wrong');
  explanationTextEl.textContent = '解析：' + currentQ.explanation;

  if (currentQ.has_caveat && currentQ.caveat_note) {
    caveatTextEl.classList.remove('hidden');
    caveatTextEl.textContent = '⚠️ 爭議備註：' + currentQ.caveat_note;
  } else {
    caveatTextEl.classList.add('hidden');
  }

  resultBoxEl.classList.remove('hidden');
  nextBtn.disabled = false;
  qIndex++;
  updateProgressUI();
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function renderReviewList() {
  if (wrongList.length === 0) {
    reviewListEl.innerHTML = '<div class="no-wrong">太厲害了，這次沒有答錯的題目！</div>';
    return;
  }
  reviewListEl.innerHTML = wrongList.map(w => `
    <div class="review-item">
      <div class="meta">
        <span class="tag">${escapeHtml(w.source)}</span>
        <span class="tag">${escapeHtml(w.topic)}</span>
        <span>第 ${w.id} 題</span>
      </div>
      <div class="question">${escapeHtml(w.question)}</div>
      <div class="review-line">你的答案：<span class="your-ans">${escapeHtml(w.yourAnswer)}</span></div>
      <div class="review-line">正確答案：<span class="correct-ans">${w.correctLetter}. ${escapeHtml(w.correctText)}</span></div>
      <div class="review-explanation">解析：${escapeHtml(w.explanation)}</div>
      ${w.has_caveat && w.caveat_note ? `<div class="caveat" style="margin-top:8px;">⚠️ 爭議備註：${escapeHtml(w.caveat_note)}</div>` : ''}
    </div>
  `).join('');
}

function showSummary() {
  quizScreen.classList.add('hidden');
  summaryScreen.classList.remove('hidden');
  summaryTotalEl.textContent = answered;
  summaryCorrectEl.textContent = correctCount;
  summaryWrongEl.textContent = answered - correctCount;
  summaryAccuracyEl.textContent = answered ? Math.round(correctCount / answered * 100) + '%' : '0%';
  renderReviewList();
}

nextBtn.addEventListener('click', showQuestion);
startBtn.addEventListener('click', startQuiz);
backToSetupBtn.addEventListener('click', showSummary);
restartSameBtn.addEventListener('click', startQuiz);
backSetupFromSummaryBtn.addEventListener('click', () => {
  summaryScreen.classList.add('hidden');
  setupScreen.classList.remove('hidden');
  updatePoolCount();
});
excludeCaveatEl.addEventListener('change', updatePoolCount);
limitEnabledEl.addEventListener('change', () => {
  limitCountEl.disabled = !limitEnabledEl.checked;
  updatePoolCount();
});
limitCountEl.addEventListener('input', updatePoolCount);

// 字體大小調整：以 rem 為基準縮放整頁文字，設定記在瀏覽器本機
const FONT_STEPS = [85, 100, 115, 130, 150, 175];
const FONT_KEY = 'quizFontScale';
const fontValEl = document.getElementById('fontVal');
const fontDownBtn = document.getElementById('fontDownBtn');
const fontUpBtn = document.getElementById('fontUpBtn');
let fontStep = 1;
try {
  const saved = FONT_STEPS.indexOf(parseInt(localStorage.getItem(FONT_KEY), 10));
  if (saved >= 0) fontStep = saved;
} catch (e) {}
function applyFont() {
  const pct = FONT_STEPS[fontStep];
  document.documentElement.style.fontSize = (16 * pct / 100) + 'px';
  fontValEl.textContent = pct + '%';
  fontDownBtn.disabled = fontStep === 0;
  fontUpBtn.disabled = fontStep === FONT_STEPS.length - 1;
  try { localStorage.setItem(FONT_KEY, pct); } catch (e) {}
}
fontDownBtn.addEventListener('click', () => { if (fontStep > 0) { fontStep--; applyFont(); } });
fontUpBtn.addEventListener('click', () => { if (fontStep < FONT_STEPS.length - 1) { fontStep++; applyFont(); } });
applyFont();

totalAllEl.textContent = QUESTIONS.length;
buildSourceCheckboxes();
updatePoolCount();
</script>
</body>
</html>
"""

html = template.replace("__DATA_JSON__", data_json)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Wrote", OUT_PATH, "with", len(rows), "questions embedded")
