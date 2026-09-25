// Общий приём заявок для yume.cloud и yumefleet.com → Telegram.
// Ключи: api/config.js (не в git) или переменные окружения TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID.
let cfg = {};
try { cfg = (await import('./config.js')).default || {}; } catch (e) { cfg = {}; }

const ALLOWED = /^https:\/\/(www\.)?(yume\.cloud|yumefleet\.com|yumefleet\.kz|yume-cloud\.github\.io|kabdyzhanzhaina-lang\.github\.io)$|^http:\/\/localhost(:\d+)?$/;

export default async function handler(req, res) {
  const origin = req.headers.origin || '';
  if (ALLOWED.test(origin)) res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Max-Age', '86400');
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'POST only' });

  const token = cfg.TELEGRAM_BOT_TOKEN || process.env.TELEGRAM_BOT_TOKEN;
  const chat = cfg.TELEGRAM_CHAT_ID || process.env.TELEGRAM_CHAT_ID;
  if (!token || !chat) return res.status(503).json({ ok: false, error: 'not_configured' });

  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = {}; } }
  b = b || {};
  if (b.website) return res.status(200).json({ ok: true });

  const clean = v => String(v ?? '').replace(/\s+/g, ' ').trim().slice(0, 200);
  const name = clean(b.name), phone = clean(b.phone), segment = clean(b.segment), page = clean(b.page), source = clean(b.source);
  if (!name || phone.replace(/\D/g, '').length < 10) return res.status(400).json({ ok: false, error: 'invalid' });

  const esc = s => s.replace(/[<>&]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]));
  const digits = phone.replace(/\D/g, '');
  const wa = digits ? `https://wa.me/${digits.replace(/^8/, '7')}` : '';
  const title = /fleet/i.test(source) || /fleet/i.test(origin) ? 'Yume Fleet' : 'yume.cloud';
  const when = new Date().toLocaleString('ru-RU', { timeZone: 'Asia/Almaty' });
  const text = [
    `<b>Новая заявка · ${title}</b>`,
    esc(name),
    `<a href="tel:+${digits}">${esc(phone)}</a>${wa ? ` · <a href="${wa}">WhatsApp</a>` : ''}`,
    segment ? esc(segment) : '',
    `${when} (Алматы)`,
  ].filter(Boolean).join('\n');

  try {
    const r = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chat, text, parse_mode: 'HTML', disable_web_page_preview: true }),
    });
    const j = await r.json();
    if (!j.ok) return res.status(502).json({ ok: false, error: 'telegram', detail: j.description });
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(502).json({ ok: false, error: 'telegram_unreachable' });
  }
}
