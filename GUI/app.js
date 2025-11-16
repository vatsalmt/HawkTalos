/* frontend/app.js */
const API_BASE = location.hostname === 'localhost'
  ? 'http://127.0.0.1:5000'       // local Flask
  : 'https://your-backend-host';  // e.g., https://hawktalos-api.onrender.com

// Helpers
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

// ===== Password Checker =====
(function initPasswordChecker() {
  const formBtn = document.querySelector('#password-checker .btn');
  const input = document.getElementById('password');
  const status = document.querySelector('#password-result .result__status');
  const meter = document.querySelector('#password-result .meter');

  if (!input || !formBtn) return;

  input.addEventListener('input', () => {
    formBtn.disabled = input.value.trim().length === 0;
    formBtn.setAttribute('aria-disabled', formBtn.disabled ? 'true' : 'false');
  });

  formBtn?.addEventListener('click', async (e) => {
    e.preventDefault();
    const password = input.value;
    if (!password) return;

    status.textContent = 'Checking...';
    meter.value = 0;

    try {
      const data = await safeFetch(`${API_BASE}/api/password/check`, {
        method: 'POST',
        body: JSON.stringify({ p: password })
      });
      // Expecting { ok: true, count: <number>, ... } from your backend
      const count = data.count ?? 0;
      status.textContent = count > 0
        ? `⚠️ Found in breaches ${count.toLocaleString()} times`
        : '✅ Not found in known breach list';
      meter.value = Math.min(100, Math.max(5, 10 + Math.log10((count || 1)) * 20));
      setText('[data-bind="kpi-passwords"]', count > 0 ? '1' : '0');
    } catch (err) {
      status.textContent = `Error: ${err.message}`;
    }
  });
})();

// ===== Email Breach Checker =====
(function initEmailChecker() {
  const formBtn = document.querySelector('#email-breach .btn');
  const input = document.getElementById('email');
  const tbody = document.querySelector('#email-result tbody');

  if (!input || !formBtn || !tbody) return;

  input.addEventListener('input', () => {
    formBtn.disabled = input.value.trim().length === 0;
    formBtn.setAttribute('aria-disabled', formBtn.disabled ? 'true' : 'false');
  });

  formBtn?.addEventListener('click', async (e) => {
    e.preventDefault();
    const email = input.value.trim();
    if (!email) return;

    tbody.innerHTML = `<tr><td colspan="3">Checking...</td></tr>`;
    try {
      const data = await safeFetch(`${API_BASE}/api/email/check`, {
        method: 'POST',
        body: JSON.stringify({ email })
      });
      const breaches = (data.hibp?.breaches || data.hibp || []);
      if (!breaches.length) {
        tbody.innerHTML = `<tr><td colspan="3">✅ No breaches found</td></tr>`;
        setText('[data-bind="kpi-emails"]', '0');
        return;
      }
      setText('[data-bind="kpi-emails"]', String(breaches.length));
      tbody.innerHTML = breaches.map(b => `
        <tr>
          <td>${b.Name || b.name || 'Breach'}</td>
          <td>${b.BreachDate || b.breachDate || '—'}</td>
          <td>${(b.DataClasses || b.dataClasses || []).join(', ') || '—'}</td>
        </tr>
      `).join('');
    } catch (err) {
      tbody.innerHTML = `<tr><td colspan="3">Error: ${err.message}</td></tr>`;
    }
  });
})();

// ===== URL Safety (Safe Browsing + PhishTank) =====
(function initUrlSafety() {
  const formBtn = document.querySelector('#url-safety .btn');
  const input = document.getElementById('url');
  const sb = document.querySelector('[data-bind="sb-verdict"]');
  const pt = document.querySelector('[data-bind="pt-verdict"]');

  if (!input || !formBtn) return;

  input.addEventListener('input', () => {
    formBtn.disabled = input.value.trim().length === 0;
    formBtn.setAttribute('aria-disabled', formBtn.disabled ? 'true' : 'false');
  });

  formBtn?.addEventListener('click', async (e) => {
    e.preventDefault();
    const url = input.value.trim();
    if (!url) return;

    sb.textContent = 'Checking...';
    pt.textContent = 'Checking...';

    try {
      const data = await safeFetch(`${API_BASE}/api/url/check`, {
        method: 'POST',
        body: JSON.stringify({ url })
      });
      const sbVerdict = data.safe_browsing?.verdict || data.safe_browsing || 'Unknown';
      const ptVerdict = data.phishtank?.verdict || data.phishtank || 'Unknown';
      sb.textContent = sbVerdict;
      pt.textContent = ptVerdict;
      setText('[data-bind="kpi-urls"]', (sbVerdict === 'Unsafe' || ptVerdict === 'Unsafe') ? '1' : '0');
    } catch (err) {
      sb.textContent = `Error: ${err.message}`;
      pt.textContent = `Error: ${err.message}`;
    }
  });
})();

// ===== KEV (CISA) =====
(async function loadKev() {
  const kevTable = document.getElementById('kev-table');
  const kevRecent = document.querySelector('[data-bind="kev-recent"]');
  if (!kevTable) return;

  try {
    const data = await safeFetch(`${API_BASE}/api/news/cisa`);
    const items = data.items || data; // adapt to backend’s shape
    if (!Array.isArray(items) || items.length === 0) return;

    // Fill main table
    kevTable.innerHTML = items.slice(0, 50).map(row => `
      <tr>
        <td><span class="badge badge--critical">${row.cveID || row.cve || 'CVE'}</span></td>
        <td>${row.vendorProject || row.vendor || '—'}</td>
        <td>${row.vulnerabilityName || row.title || '—'}</td>
        <td>${row.dateAdded || '—'}</td>
        <td>${row.dueDate || '—'}</td>
      </tr>
    `).join('');

    // Fill “recent” list
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
  }
})();