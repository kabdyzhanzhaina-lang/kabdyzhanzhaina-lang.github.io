// Vercel serverless proxy for the eGov debtors registry.
// Keeps the API token on the server: set YUME_API_TOKEN in Vercel → Settings → Environment Variables.
// Optional: YUME_TENANT_ID (default 4), YUME_API_BASE (default https://api.yume.cloud).
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') return res.status(405).json({ detail: 'GET only' });

  const q = String((req.query && req.query.q) || '').trim();
  if (q.length < 2 || q.length > 64) return res.status(400).json({ detail: 'Укажите ИИН, БИН или ФИО' });

  const base = process.env.YUME_API_BASE || 'https://api.yume.cloud';
  const headers = { Accept: 'application/json', 'X-Tenant-Id': process.env.YUME_TENANT_ID || '4' };
  const token = process.env.YUME_API_TOKEN;
  if (token) headers.Authorization = /^(Bearer|Token|JWT) /i.test(token) ? token : `Bearer ${token}`;

  try {
    const upstream = await fetch(`${base}/v1/crm/integrations/egov/${encodeURIComponent(q)}`, { headers });
    const text = await upstream.text();
    res.status(upstream.status);
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    if (upstream.status === 401 && !token) {
      return res.send(JSON.stringify({ detail: 'no_token', upstream: text.slice(0, 200) }));
    }
    return res.send(text);
  } catch (e) {
    return res.status(502).json({ detail: 'upstream_unavailable' });
  }
}
