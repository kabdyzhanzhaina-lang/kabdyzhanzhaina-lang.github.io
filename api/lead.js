// Sends demo-form leads to a Telegram chat via your bot.
// Env vars (Vercel → Settings → Environment Variables):
//   TELEGRAM_BOT_TOKEN  — token from @BotFather
//   TELEGRAM_CHAT_ID    — chat/group id where the bot should post (bot must be a member)
// Ключи берутся из api/config.js (см. api/config.example.js) или из переменных окружения Vercel.
let cfg = {};
try { cfg = (await import('./config.js')).default || {}; } catch (e) { cfg = {}; }

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'POST only' });

  const token = cfg.TELEGRAM_BOT_TOKEN || process.env.TELEGRAM_BOT_TOKEN;
  const chat = cfg.TELEGRAM_CHAT_ID || process.env.TELEGRAM_CHAT_ID;
  if (!token || !chat) return res.status(503).json({ ok: false, error: 'not_configured' });

  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = {}; } }
  b = b || {};
  if (b.website) return res.status(200).json({ ok: true }); // honeypot filled by a bot

  const clean = v => String(v ?? '').replace(/\s+/g, ' ').trim().slice(0, 200);
  const name = clean(b.name), phone = clean(b.phone), segment = clean(b.segment), page = clean(b.page), source = clean(b.source);
  if (!name || phone.replace(/\D/g, '').length < 10) return res.status(400).json({ ok: false, error: 'invalid' });

  const esc = s => s.replace(/[<>&]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]));
  const digits = phone.replace(/\D/g, '');
  const wa = digits ? `https://wa.me/${digits.replace(/^8/, '7')}` : '';
  const when = new Date().toLocaleString('ru-RU', { timeZone: 'Asia/Almaty' });
  const text = [
    '🟣 <b>Новая заявка с yume.cloud</b>',
    `👤 ${esc(name)}`,
    `📞 <a href="tel:+${digits}">${esc(phone)}</a>${wa ? ` · <a href="${wa}">WhatsApp</a>` : ''}`,
    segment ? `🏷 ${esc(segment)}` : '',
    source ? `📍 ${esc(source)}` : '',
    page ? `🔗 ${esc(page)}` : '',
    `🕒 ${when} (Алматы)`,
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
