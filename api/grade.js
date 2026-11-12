// Vercel serverless function: grades the child's answer with Claude.
// Needs ANTHROPIC_API_KEY in the project's environment variables. Without it, HEAD/POST return 501 and the games fall back to keyword grading.
module.exports = async function handler(req, res) {
  const key = process.env.ANTHROPIC_API_KEY;
  if (req.method === "HEAD" || req.method === "GET") { res.status(key ? 200 : 501).end(); return; }
  if (req.method !== "POST") { res.status(405).end(); return; }
  if (!key) { res.status(501).json({ error: "no key" }); return; }
  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const prompt = String((body && body.prompt) || "").slice(0, 6000);
  if (!prompt) { res.status(400).json({ error: "no prompt" }); return; }
  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model: process.env.RAFIQ_MODEL || "claude-sonnet-5-5", max_tokens: 400, messages: [{ role: "user", content: prompt }] })
    });
    const j = await r.json();
    const text = (j.content || []).map(c => c.text || "").join("");
    res.setHeader("cache-control", "no-store");
    res.status(200).json({ text });
  } catch (e) {
    res.status(502).json({ error: "upstream" });
  }
}
