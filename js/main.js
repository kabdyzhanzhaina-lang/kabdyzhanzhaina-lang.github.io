/* yume.cloud — interactions & animations (no dependencies) */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wait = ms => new Promise(r => setTimeout(r, ms));

  /* ---------- NAV ---------- */
  const nav = $('.nav');
  const hero = $('.hero');
  const onScroll = () => {
    nav.classList.toggle('is-scrolled', scrollY > 24);
    $('.to-top')?.classList.toggle('is-on', scrollY > 900);
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  $('.nav__burger')?.addEventListener('click', () => nav.classList.toggle('is-open'));
  $$('.nav__menu a').forEach(a => a.addEventListener('click', () => nav.classList.remove('is-open')));

  /* ---------- HERO: cursor glow + tilt ---------- */
  if (hero && matchMedia('(pointer:fine)').matches && !reduced) {
    const glow = $('.hero__glow'); const frame = $('.hero__frame');
    hero.addEventListener('mousemove', e => {
      const r = hero.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      glow.style.setProperty('--gx', `${x * 100}%`); glow.style.setProperty('--gy', `${y * 100}%`);
      frame.style.setProperty('--rx', `${8 - y * 6}deg`);
      frame.style.transform = `rotateX(${8 - y * 6}deg) rotateY(${(x - .5) * 4}deg)`;
    });
    hero.addEventListener('mouseleave', () => { frame.style.transform = ''; });
  }
  $$('.float').forEach(f => f.addEventListener('animationend', () => f.classList.add('is-live'), { once: true }));

  /* ---------- Button light follow ---------- */
  $$('.btn').forEach(b => b.addEventListener('pointermove', e => {
    const r = b.getBoundingClientRect();
    b.style.setProperty('--mx', `${e.clientX - r.left}px`); b.style.setProperty('--my', `${e.clientY - r.top}px`);
  }));
  $$('.seg').forEach(c => c.addEventListener('pointermove', e => {
    const r = c.getBoundingClientRect();
    c.style.setProperty('--mx', `${e.clientX - r.left}px`); c.style.setProperty('--my', `${e.clientY - r.top}px`);
  }));

  /* ---------- Reveal on scroll ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }), { threshold: .12, rootMargin: '0px 0px -8% 0px' });
  $$('[data-reveal]').forEach(el => io.observe(el));
  $$('[data-stagger]').forEach(g => $$(':scope > *', g).forEach((c, i) => {
    c.setAttribute('data-reveal', g.dataset.stagger || ''); c.style.setProperty('--d', `${i * .09}s`); io.observe(c);
  }));

  /* ---------- Counters ---------- */
  const fmt = n => n.toLocaleString('ru-RU');
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return; cio.unobserve(e.target);
    const el = e.target, to = +el.dataset.count, suf = el.dataset.suffix || '', dur = 1600, t0 = performance.now();
    const tick = t => {
      const p = Math.min(1, (t - t0) / dur), k = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(to * k)) + suf;
      if (p < 1) requestAnimationFrame(tick);
    };
    reduced ? (el.textContent = fmt(to) + suf) : requestAnimationFrame(tick);
  }), { threshold: .6 });
  $$('[data-count]').forEach(el => cio.observe(el));

  /* ---------- Flow progress line ---------- */
  const flow = $('.flow');
  if (flow) {
    const line = $('.flow__line i', flow), steps = $$('.step', flow);
    const upd = () => {
      const r = flow.getBoundingClientRect(), vh = innerHeight;
      const p = Math.min(1, Math.max(0, (vh * .8 - r.top) / (r.height + vh * .2)));
      line.style.setProperty('--p', p);
      steps.forEach((s, i) => s.classList.toggle('is-on', p >= (i + .5) / steps.length));
    };
    addEventListener('scroll', upd, { passive: true }); upd();
  }

  /* ---------- Feature tabs (auto-rotate) ---------- */
  const tabs = $$('.tab'), panes = $$('.pane');
  if (tabs.length) {
    let cur = 0, timer;
    const show = i => {
      cur = i;
      tabs.forEach((t, k) => t.classList.toggle('is-active', k === i));
      panes.forEach((p, k) => p.classList.toggle('is-active', k === i));
    };
    const auto = () => { clearInterval(timer); if (!reduced) timer = setInterval(() => show((cur + 1) % tabs.length), 6000); };
    tabs.forEach((t, i) => t.addEventListener('click', () => { show(i); auto(); }));
    const fio = new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? auto() : clearInterval(timer)), { threshold: .3 });
    fio.observe($('.feat'));
    show(0);
  }

  /* ---------- Client check demo ---------- */
  const demo = $('.demo');
  if (demo) {
    const inp = $('.demo__val', demo), prog = $('.demo__prog i', demo), res = $$('.demo__res', demo);
    const scen = [
      { iin: '900412300587', bad: true },
      { iin: '870925401122', bad: false },
    ];
    let k = 0, running = false;
    const run = async () => {
      if (running) return; running = true;
      const s = scen[k % scen.length]; k++;
      res.forEach(r => r.classList.remove('is-in')); prog.style.width = '0';
      inp.textContent = '';
      for (const ch of s.iin.replace(/(\d{6})(\d{3})(\d{3})/, '$1 $2 $3')) { inp.textContent += ch; await wait(reduced ? 0 : 55); }
      await wait(200); prog.style.width = '100%'; await wait(900);
      res[s.bad ? 0 : 1].classList.add('is-in'); running = false;
    };
    $('.demo__again', demo)?.addEventListener('click', run);
    const dio = new IntersectionObserver(es => { if (es[0].isIntersecting) { run(); dio.disconnect(); } }, { threshold: .5 });
    dio.observe(demo);
  }

  /* ---------- AI chat loop ---------- */
  const chat = $('#ai .chat__log');
  if (chat) {
    const script = [
      { me: true, t: 'Что должны вернуть сегодня и кто уже просрочил?' },
      { me: false, t: 'Сегодня возврат по 7 арендам. Просрочены две:', rows: [['Леса рамные, 12 секций', 'Асхат М. · 1 день · +4 500 ₸'], ['Плиткорез Rubi', 'ТОО «Ремстрой» · 3 дня · +9 000 ₸']], tail: 'Отправить обоим напоминание в WhatsApp?' },
      { me: true, t: 'Да. И сколько мы заработали на перфораторах в сентябре?' },
      { me: false, t: 'Напоминания отправлены. Перфораторы за сентябрь: 48 аренд, 612 000 ₸ выручки, загрузка 71%. Это на 18% больше августа.' },
    ];
    const mk = (m) => {
      const d = document.createElement('div'); d.className = 'msg ' + (m.me ? 'msg--me' : 'msg--ai');
      d.textContent = m.t;
      (m.rows || []).forEach(([a, b]) => {
        const r = document.createElement('div'); r.className = 'msg__row';
        r.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><div><b>${a}</b><small>${b}</small></div>`;
        d.append(r);
      });
      if (m.tail) { const p = document.createElement('div'); p.style.marginTop = '8px'; p.textContent = m.tail; d.append(p); }
      return d;
    };
    const typing = () => { const d = document.createElement('div'); d.className = 'msg msg--ai typing'; d.innerHTML = '<i></i><i></i><i></i>'; return d; };
    let started = false;
    const play = async () => {
      while (true) {
        chat.innerHTML = '';
        for (const m of script) {
          if (!m.me) { const t = typing(); chat.append(t); await wait(reduced ? 0 : 1100); t.remove(); }
          chat.append(mk(m)); await wait(reduced ? 200 : (m.me ? 900 : 2200));
        }
        await wait(4500);
      }
    };
    const aio = new IntersectionObserver(es => { if (es[0].isIntersecting && !started) { started = true; play(); } }, { threshold: .3 });
    aio.observe(chat);
  }

  /* ---------- Pricing switch ---------- */
  const sw = $$('.switch button');
  sw.forEach(b => b.addEventListener('click', () => {
    sw.forEach(x => x.classList.toggle('is-on', x === b));
    const yearly = b.dataset.period === 'year';
    $$('[data-month]').forEach(p => {
      const v = +(yearly ? p.dataset.year : p.dataset.month);
      const from = +p.textContent.replace(/\D/g, '') || v, t0 = performance.now();
      const tick = t => { const k = Math.min(1, (t - t0) / 500); p.textContent = fmt(Math.round(from + (v - from) * k)) + ' ₸'; if (k < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
    });
  }));

  /* ---------- FAQ ---------- */
  $$('.q button').forEach(b => b.addEventListener('click', () => {
    const q = b.parentElement, open = q.classList.contains('is-open');
    $$('.q.is-open').forEach(x => x.classList.remove('is-open'));
    if (!open) q.classList.add('is-open');
  }));

  /* ---------- Form ---------- */
  const form = $('.form');
  form?.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = $('button[type=submit]', form), name = $('#name', form), phone = $('#phone', form);
    const digits = (phone?.value || '').replace(/\D/g, '');
    if (!name?.value.trim()) { name.focus(); name.classList.add('is-invalid'); return; }
    if (digits.length < 11) { phone.focus(); phone.classList.add('is-invalid'); return; }
    const label = btn.textContent; btn.disabled = true; btn.textContent = 'Отправляем…';
    const payload = { name: name.value.trim(), phone: phone.value.trim(), segment: $('#seg', form)?.value || '', page: location.pathname, source: document.title, website: $('input[name=website]', form)?.value || '' };
    try {
      const r = await fetch('https://yume-cloud-zzydfr.vercel.app/api/lead/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok || !j.ok) throw new Error(j.error || r.status);
      form.classList.add('is-done');
      try { window.gtag && gtag('event', 'generate_lead', { segment: payload.segment }); window.fbq && fbq('track', 'Lead'); } catch (x) {}
    } catch (err) {
      btn.disabled = false; btn.textContent = label;
      const msg = `Здравствуйте! Хочу демо Yume.\nИмя: ${payload.name}\nТелефон: ${payload.phone}\nСфера: ${payload.segment}`;
      window.open('https://wa.me/77779479990?text=' + encodeURIComponent(msg), '_blank', 'noopener');
      let m = $('.form__err', form);
      if (!m) { m = document.createElement('p'); m.className = 'form__err'; btn.after(m); }
      m.textContent = 'Открыли WhatsApp с текстом заявки. Если окно не открылось, напишите на +7 777 947 99 90';
    }
  });
  $$('.form input').forEach(i => i.addEventListener('input', () => i.classList.remove('is-invalid')));
  $('#phone')?.addEventListener('input', e => {
    let d = e.target.value.replace(/\D/g, '').replace(/^8/, '7').slice(0, 11);
    if (d && d[0] !== '7') d = '7' + d;
    const p = [d.slice(1, 4), d.slice(4, 7), d.slice(7, 9), d.slice(9, 11)];
    e.target.value = d ? '+7' + (p[0] ? ' ' + p[0] : '') + (p[1] ? ' ' + p[1] : '') + (p[2] ? ' ' + p[2] : '') + (p[3] ? ' ' + p[3] : '') : '';
  });

  /* ---------- AI example buttons -> scroll to demo ---------- */
  $$('.ai__ex button').forEach(b => b.addEventListener('click', () => {
    const inp = $('.chat__input span'); if (inp) { inp.textContent = b.textContent.replace(/[«»]/g, ''); inp.style.color = 'var(--ink)'; }
  }));

  /* ---------- to top ---------- */
  $('.to-top')?.addEventListener('click', () => scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }));
})();
