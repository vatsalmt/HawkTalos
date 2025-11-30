/* frontend/app.js */

// =========================
// API Base URL
// =========================
const API_BASE = (location.hostname === 'localhost' || location.hostname === '127.0.0.1')
  ? 'http://127.0.0.1:5000'
  : 'https://your-backend-host';

// =========================
// Helpers
// =========================
async function safeFetch(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  if (!res.ok) {
    const msg = await res.text().catch(() => res.statusText);
    throw new Error(`HTTP ${res.status}: ${msg}`);
  }
  return res.json();
}

function $(sel) { return document.querySelector(sel); }
function setText(sel, txt) { const el = $(sel); if (el) el.textContent = txt; }

// =========================
// Password Checker
// =========================
(function initPasswordChecker() {
  const input = $('#password');
  const formBtn = $('#password-checker .btn');
  const status = $('#password-result .result__status');
  const meter = $('#password-result .meter');

  if (!input || !formBtn) return;

  input.addEventListener('input', () => {
    formBtn.disabled = input.value.trim() === '';
  });

  formBtn.addEventListener('click', async (e) => {
    e.preventDefault();
    const password = input.value;
    if (!password) return;

    status.textContent = 'Checking...';
    meter.value = 0;

    try {
      const response = await safeFetch(`${API_BASE}/api/password/check`, {
        method: 'POST',
        body: JSON.stringify({ p: password })
      });
      
      
      const data = response.data || {};
      const count = data.count || 0;
      const pwned = data.pwned || false;
      const message = data.message || '';
      
      status.textContent = message || (count > 0
        ? `⚠️ Found in breaches ${count.toLocaleString()} times`
        : '✅ Not found in known breach list');
      
      meter.value = Math.min(100, Math.max(5, 10 + Math.log10(count || 1) * 20));
      setText('[data-bind="kpi-passwords"]', pwned ? '1' : '0');
    } catch (err) {
      status.textContent = `Error: ${err.message}`;
    }
  });
})();

// =========================
// Email Breach Checker
// =========================
(function initEmailChecker() {
  const input = $('#email');
  const formBtn = $('#email-breach .btn');
  const tbody = $('#email-result tbody');

  if (!input || !formBtn || !tbody) return;

  input.addEventListener('input', () => {
    formBtn.disabled = input.value.trim() === '';
  });

  formBtn.addEventListener('click', async (e) => {
    e.preventDefault();
    const email = input.value.trim();
    if (!email) return;

    tbody.innerHTML = `<tr><td colspan="3">Checking...</td></tr>`;

    try {
      const response = await safeFetch(`${API_BASE}/api/email/check`, {
        method: 'POST',
        body: JSON.stringify({ email })
      });

      
      const hibpData = response.hibp?.data || {};
      const hibpBreaches = hibpData.breaches || [];
      
     
      const leakData = response.leakcheck?.data || {};
      
      
      let hasBreaches = false;
      let breachCount = 0;
      let tableHTML = '';
      
      
      if (response.hibp?.ok && hibpBreaches.length > 0) {
        hasBreaches = true;
        breachCount = hibpBreaches.length;
        tableHTML = hibpBreaches.map(b => `
          <tr>
            <td>${b.Name || b.name || 'Breach'}</td>
            <td>${b.BreachDate || b.breachDate || '—'}</td>
            <td>${(b.DataClasses || b.dataClasses || []).join(', ') || '—'}</td>
          </tr>
        `).join('');
      }
      
      else if (response.leakcheck?.ok) {
        
        if (leakData.found === true || leakData.sources || leakData.result) {
          hasBreaches = true;
          
          const sources = leakData.sources || leakData.result || [];
          breachCount = sources.length || 1;
          
          if (Array.isArray(sources) && sources.length > 0) {
            tableHTML = sources.map(s => `
              <tr>
                <td>${s.name || s.source || 'Data Breach'}</td>
                <td>${s.date || s.breach_date || '—'}</td>
                <td>${s.type || 'Email/Password'}</td>
              </tr>
            `).join('');
          } else {
            
            tableHTML = `
              <tr>
                <td>Data Breach Detected</td>
                <td>—</td>
                <td>Check LeakCheck for details</td>
              </tr>
            `;
          }
        }
      }
      
      
      if (hasBreaches) {
        tbody.innerHTML = tableHTML || `<tr><td colspan="3">⚠️ Breaches found (check details)</td></tr>`;
        setText('[data-bind="kpi-emails"]', String(breachCount));
      } else {
        tbody.innerHTML = `<tr><td colspan="3">✅ No breaches found</td></tr>`;
        setText('[data-bind="kpi-emails"]', '0');
      }
      
    } catch (err) {
      tbody.innerHTML = `<tr><td colspan="3">Error: ${err.message}</td></tr>`;
    }
  });
})();

// =========================
// URL Safety Checker
// =========================
(function initUrlSafety() {
  const input = $('#url');
  const formBtn = $('#url-safety .btn');
  const sb = $('[data-bind="sb-verdict"]');
  const pt = $('[data-bind="pt-verdict"]');
  const icon = formBtn?.querySelector('i'); 

  if (!input || !formBtn) return;

  input.addEventListener('input', () => {
    formBtn.disabled = input.value.trim() === '';
  });

  formBtn.addEventListener('click', async (e) => {
    e.preventDefault();
    const url = input.value.trim();
    if (!url) return;

    
    if (icon) icon.className = 'icon icon--loading';
    sb.textContent = 'Checking...';
    pt.textContent = 'Checking...';

    try {
      const response = await safeFetch(`${API_BASE}/api/url/check`, {
        method: 'POST',
        body: JSON.stringify({ url })
      });

      console.log('Full URL response:', response);

      
      const data = response.data || {};
      const verdict = data.verdict || 'Unknown';
      const threats = data.threat_types || [];
      
     
      const sbResult = data.google_safe_browsing || {};
      const sbVerdict = sbResult.ok && sbResult.data?.matches ? 'Malicious' : 
                        sbResult.ok ? 'Safe' : 'Unknown';
      
      
      const ptResult = data.phishtank || {};
      const ptVerdict = ptResult.ok && ptResult.data?.found ? 'Malicious' : 
                        ptResult.ok ? 'Safe' : 'Unknown';

      sb.textContent = sbVerdict;
      pt.textContent = ptVerdict;

      
      if (icon) icon.className = 'icon icon--scan';

      
      setText('[data-bind="kpi-urls"]', verdict === 'malicious' ? '1' : '0');

    } catch (err) {
      sb.textContent = `Error: ${err.message}`;
      pt.textContent = `Error: ${err.message}`;

      
      if (icon) icon.className = 'icon icon--error';
    }
  });
})();

// =========================
// KEV (CISA)
// =========================
(async function loadKev() {
  const kevTable = $('#kev-table');
  const kevRecent = $('[data-bind="kev-recent"]');
  if (!kevTable) return;

  try {
    const response = await safeFetch(`${API_BASE}/api/news/cisa`);
    
    
    const data = response.data || {};
    const items = data.vulnerabilities || data.items || [];

    if (!Array.isArray(items) || items.length === 0) {
      kevTable.innerHTML = '<tr><td colspan="5">No vulnerabilities available</td></tr>';
      return;
    }

    kevTable.innerHTML = items.slice(0, 50).map(r => `
      <tr>
        <td><span class="badge badge--critical">${r.cveID || r.cve || 'CVE'}</span></td>
        <td>${r.vendorProject || r.vendor || '—'}</td>
        <td>${r.vulnerabilityName || r.title || '—'}</td>
        <td>${r.dateAdded || '—'}</td>
        <td>${r.dueDate || '—'}</td>
      </tr>
    `).join('');

    if (kevRecent) {
      kevRecent.innerHTML = items.slice(0, 5).map(r => `
        <li class="list__row">
          <span class="badge badge--critical">${r.cveID || 'CVE'}</span>
          <span class="muted">${r.vulnerabilityName || r.title || ''}</span>
          <time class="muted" datetime="${r.dateAdded || ''}">${r.dateAdded || ''}</time>
        </li>
      `).join('');
    }

    setText('[data-bind="kpi-kev"]', String(items.length));
  } catch (err) {
    console.error('KEV error:', err);
    kevTable.innerHTML = '<tr><td colspan="5">Error loading vulnerabilities</td></tr>';
  }
})();

// =========================
// CyberQuest Quiz
// =========================
(function quizModule() {
  const startPanel = $('#quiz-start-panel');
  const questionPanel = $('#quiz-question-panel');
  const resultPanel = $('#quiz-result-panel');

  const startForm = $('#quiz-start-form');
  const startBtn = $('#quiz-start-btn');
  const usernameInput = $('#quiz-username');
  const diffInput = $('#quiz-difficulty');

  const qText = $('#quiz-question-text');
  const qOptions = $('#quiz-answer-form');
  const qCategory = $('#quiz-category');
  const qDiff = $('#quiz-diff');
  const qPrev = $('#quiz-prev');
  const qNext = $('#quiz-next');
  const qSubmit = $('#quiz-submit');
  const qProgress = $('#quiz-progress');
  const qProgressText = $('#quiz-progress-text');

  const rScore = $('#quiz-score');
  const rPct = $('#quiz-percentage');
  const rTier = $('#quiz-tier');
  const rQuote = $('#quiz-quote');
  const rTableBody = $('#quiz-breakdown tbody');
  const rRestart = $('#quiz-restart');
  const rCert = $('#quiz-certificate');

  let sessionId = null, questions = [], answers = {}, idx = 0, username = 'Anonymous';

  async function apiPost(path, payload = {}) {
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const json = await res.json().catch(() => ({ ok: false, error: 'Bad JSON' }));
    if (!res.ok) throw new Error(json.error || `${res.status} ${res.statusText}`);
    return json;
  }

  function showPanel(panel) {
    [startPanel, questionPanel, resultPanel].forEach(p => p && (p.hidden = true));
    if (panel) panel.hidden = false;
  }

  function updateProgress() {
    const total = questions.length || 1;
    const pct = Math.round(((idx + 1) / total) * 100);
    qProgress.value = pct;
    qProgressText.textContent = `Question ${idx + 1} / ${total}`;
  }

  function renderQuestion() {
    const q = questions[idx];
    if (!q) return;

    qText.textContent = q.question;
    qCategory.textContent = `Category: ${q.category || 'General'}`;
    qDiff.textContent = `Difficulty: ${q.difficulty || 'mixed'}`;
    updateProgress();

    qOptions.innerHTML = '';
    const selected = answers[q.id] || null;

    
    const optionsArray = Array.isArray(q.options) ? q.options : Object.values(q.options || {});
    
    optionsArray.forEach((opt, i) => {
      const letter = String.fromCharCode(65 + i);
      const id = `opt-${q.id}-${letter}`;
      const row = document.createElement('label');
      row.className = 'quiz__option';
      row.setAttribute('for', id);
      row.innerHTML = `
        <input type="radio" id="${id}" name="q-${q.id}" value="${letter}" ${selected === letter ? 'checked' : ''} />
        <div><strong>${letter}.</strong> ${opt}</div>
        <div></div>
      `;
      qOptions.appendChild(row);
    });

    qPrev.disabled = (idx === 0);
    const last = (idx === questions.length - 1);
    qNext.hidden = last;
    qSubmit.hidden = !last;

    
    qOptions.querySelectorAll('input[type="radio"]').forEach(r => {
      r.addEventListener('change', e => {
        answers[q.id] = e.target.value;
      });
    });
  }

  async function startQuiz(e) {
    e.preventDefault();
    startBtn.disabled = true;
    username = (usernameInput.value || 'Anonymous').trim();
    const difficulty = diffInput.value || 'mixed';

    try {
      const resp = await apiPost('/api/quiz/start', { username, difficulty });
      if (!resp.ok) throw new Error(resp.error || 'Failed to start quiz');
      const data = resp.data || {};
      sessionId = data.session_id;
      questions = data.questions || [];
      answers = {}; idx = 0;
      if (!questions.length) throw new Error('No questions returned by server.');
      showPanel(questionPanel);
      renderQuestion();
    } catch (err) {
      alert(`Unable to start quiz: ${err.message}`);
    } finally {
      startBtn.disabled = false;
    }
  }

  async function submitQuiz() {
    questions.forEach(q => { if (!(q.id in answers)) answers[q.id] = ''; });
    try {
      const resp = await apiPost('/api/quiz/submit', { username, session_id: sessionId, answers });
      if (!resp.ok) throw new Error(resp.error || 'Submit failed');
      const data = resp.data || {};

      rScore.textContent = `${data.score} / ${data.total}`;
      rPct.textContent = `${data.percentage}%`;
      rTier.textContent = data.performance_tier || '—';
      rQuote.textContent = data.motivational_quote || '';

      rCert.hidden = !data.certificate_available;
      if (!rCert.hidden) {
        rCert.onclick = () => {
          const url = `${API_BASE}/api/quiz/certificate/${encodeURIComponent(sessionId)}?username=${encodeURIComponent(username)}`;
          window.open(url, '_blank');
        };
      }

      const rows = (data.results || []).map((r, i) => {
        const ok = r.is_correct ? 'Correct' : 'Incorrect';
        const chip = r.is_correct ? 'quiz__chip quiz__chip--ok' : 'quiz__chip quiz__chip--bad';
        return `
          <tr>
            <td>${i+1}</td>
            <td>${r.question}</td>
            <td>${r.your_answer || '—'}</td>
            <td>${r.correct_answer || '—'}</td>
            <td><span class="${chip}">${ok}</span></td>
          </tr>
        `;
      }).join('');
      rTableBody.innerHTML = rows || `<tr><td colspan="5">No details available.</td></tr>`;
      showPanel(resultPanel);
    } catch (err) {
      alert(`Unable to submit quiz: ${err.message}`);
    }
  }

  function restartQuiz() {
    sessionId = null; questions = []; answers = {}; idx = 0;
    startForm.reset();
    showPanel(startPanel);
  }

  
  startForm?.addEventListener('submit', startQuiz);
  qPrev?.addEventListener('click', () => { if (idx > 0) { idx--; renderQuestion(); } });
  qNext?.addEventListener('click', () => {
    const q = questions[idx];
    const sel = document.querySelector(`input[name="q-${q.id}"]:checked`);
    if (!sel) { alert('Please select an answer to continue.'); return; }
    answers[q.id] = sel.value;
    if (idx < questions.length - 1) { idx++; renderQuestion(); }
  });
  qSubmit?.addEventListener('click', () => {
    const q = questions[idx];
    const sel = document.querySelector(`input[name="q-${q.id}"]:checked`);
    if (sel) answers[q.id] = sel.value;
    submitQuiz();
  });
  rRestart?.addEventListener('click', restartQuiz);
})();