/* Live client check: eGov debtors registry + Yume blacklist (same API as the previous site) */
(() => {
  const root = document.querySelector('[data-check]');
  if (!root) return;
  const API_EGOV = '/api/egov/?q=';
  const API_BL = 'https://api.yume.cloud/v1/blacklist/check/';
  const HEADERS = { 'X-Tenant-Id': '4' };
  const PAGE = 10;
  const $ = s => root.querySelector(s);
  const input = $('input'), btn = $('.cw__btn'), results = $('.cw__results');
  const egovBox = $('[data-box="egov"]'), blBox = $('[data-box="bl"]');
  let egovAll = [], egovPage = 1, blPage = 1, lastQ = '';
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmtDate = v => { if (!v) return ''; const d = new Date(v); return isNaN(d) ? esc(v) : d.toLocaleDateString('ru-RU'); };
  const fmtMoney = v => (v == null || isNaN(+v)) ? '0 ₸' : Math.round(+v).toLocaleString('ru-RU') + ' ₸';
  const digitsOnly = q => q.replace(/\D/g, '');

  const setState = (box, state, html) => {
    const body = box.querySelector('.cw__body');
    box.dataset.state = state;
    body.innerHTML = html;
  };
  const loading = box => setState(box, 'loading', '<div class="cw__loader"><i></i>Проверяем…</div>');
  const empty = (box, title, sub) => setState(box, 'ok', `<div class="cw__ok"><i><svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></i><b>${title}</b><span>${sub}</span></div>`);
  const fail = (box, msg) => setState(box, 'error', `<div class="cw__err"><i>!</i><b>${msg}</b><span>Попробуйте ещё раз через минуту. Внутри платформы Yume проверка выполняется автоматически при каждой аренде.</span></div>`);
  const table = (cols, rows) => `<div class="cw__tablewrap"><table class="cw__table"><thead><tr>${cols.map(c => `<th>${c}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  const pager = (page, pages, key) => pages > 1 ? `<div class="cw__pager"><button data-pg="${key}:${page - 1}" ${page <= 1 ? 'disabled' : ''}>‹</button><span>${page} / ${pages}</span><button data-pg="${key}:${page + 1}" ${page >= pages ? 'disabled' : ''}>›</button></div>` : '';

  /* ---- eGov registry (АИС ОИП) ---- */
  const renderEgov = () => {
    if (!egovAll.length) return empty(egovBox, 'В реестре должников записей нет', 'Исполнительных производств по этому запросу не найдено');
    const pages = Math.ceil(egovAll.length / PAGE);
    const slice = egovAll.slice((egovPage - 1) * PAGE, egovPage * PAGE);
    const rows = slice.map(e => [
      `<b>${esc([e.debtorSurname, e.debtorName, e.debtorSecondname].filter(Boolean).join(' ') || e.debtorTitle || '—')}</b>`,
      fmtDate(e.ipStartDate),
      esc([e.disaDepartmentNameRu, [e.officerName, e.officerSurname].filter(Boolean).join(' ')].filter(Boolean).join(', ')),
      esc(e.ilOrganRu || ''),
      e.banStartDate ? '<span class="cw__badge cw__badge--bad">Выезд запрещён</span>' : '<span class="cw__badge cw__badge--ok">Запрета нет</span>',
      esc(e.recovererTitle || ''),
      `<b class="nowrap">${fmtMoney(e.recoveryAmount)}</b>`,
    ]);
    setState(egovBox, 'found', `<div class="cw__count"><span class="cw__badge cw__badge--bad">Найдено: ${egovAll.length}</span></div>` +
      table(['Должник', 'Дата ИП', 'Орган ИП, судебный исполнитель', 'Орган, выдавший документ', 'Запрет на выезд', 'Взыскатель', 'Сумма взыскания'], rows) + pager(egovPage, pages, 'egov'));
  };
  let egovCtl;
  const checkEgov = async q => {
    egovCtl?.abort(); egovCtl = new AbortController();
    loading(egovBox);
    try {
      const r = await fetch(API_EGOV + encodeURIComponent(q), { signal: egovCtl.signal });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const j = await r.json();
      egovAll = (Array.isArray(j) ? j : (j?.results || [])).slice().sort((a, b) => new Date(b.ipStartDate || 0) - new Date(a.ipStartDate || 0));
      egovPage = 1; renderEgov();
    } catch (e) {
      if (e.name === 'AbortError') return;
      fail(egovBox, /HTTP 401|HTTP 403/.test(e.message) ? 'Реестр eGov сейчас доступен только внутри платформы' : 'Реестр eGov временно не отвечает');
    }
  };

  /* ---- Yume blacklist ---- */
  let blCtl;
  const checkBl = async (q, page) => {
    blCtl?.abort(); blCtl = new AbortController();
    loading(blBox);
    try {
      const u = new URL(API_BL); u.searchParams.set('search', q); u.searchParams.set('page', page); u.searchParams.set('pageSize', PAGE);
      const r = await fetch(u, { headers: HEADERS, signal: blCtl.signal });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const j = await r.json();
      const rows = [];
      for (const rec of (j.results || [])) for (const it of (rec.records || [])) rows.push([
        `<b>${esc(it.name || rec.canonical_name || '—')}</b>`,
        esc((rec.canonical_iin || '').slice(0, 4)) + '********',
        esc(it.company_name || ''),
        esc(it.company_type || ''),
        '<span class="muted">Подробности видны внутри платформы Yume</span>',
        fmtDate(it.added_at),
      ]);
      if (!rows.length) return empty(blBox, 'Всё чисто', 'В чёрном списке прокатчиков записей не найдено');
      const pages = Math.max(1, Math.ceil((j.count || rows.length) / PAGE));
      blPage = j.page || page;
      setState(blBox, 'found', `<div class="cw__count"><span class="cw__badge cw__badge--bad">В чёрном списке: ${j.count || rows.length}</span></div>` +
        table(['ФИО', 'ИИН', 'Кто добавил', 'Деятельность', 'Причина', 'Дата'], rows) + pager(blPage, pages, 'bl'));
    } catch (e) {
      if (e.name === 'AbortError') return;
      fail(blBox, /HTTP 429/.test(e.message) ? 'Слишком много запросов' : 'Чёрный список временно не отвечает');
    }
  };

  const run = () => {
    const q = input.value.trim();
    if (q.length < 2) { input.focus(); input.classList.add('is-shake'); setTimeout(() => input.classList.remove('is-shake'), 500); return; }
    lastQ = q; results.hidden = false; btn.disabled = true; btn.textContent = 'Проверяем…';
    const d = digitsOnly(q);
    Promise.allSettled([checkEgov(d.length === 12 ? d : q), checkBl(q, 1)]).then(() => { btn.disabled = false; btn.textContent = 'Проверить'; });
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
    try { window.gtag && gtag('event', 'client_check', { method: d.length === 12 ? 'iin' : 'text' }); } catch (e) {}
  };
  btn.addEventListener('click', run);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') run(); if (e.key === 'Escape') { input.value = ''; results.hidden = true; } });
  root.addEventListener('click', e => {
    const b = e.target.closest('[data-pg]'); if (!b || b.disabled) return;
    const [key, p] = b.dataset.pg.split(':');
    if (key === 'egov') { egovPage = +p; renderEgov(); } else checkBl(lastQ, +p);
  });
  root.querySelectorAll('[data-example]').forEach(b => b.addEventListener('click', () => { input.value = b.dataset.example; run(); }));
})();
