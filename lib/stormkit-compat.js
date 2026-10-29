const MAX_BODY_BYTES = 1024 * 1024;

async function parseBody(req) {
  if (req.body !== undefined && req.body !== null) return req.body;
  if (!["POST", "PUT", "PATCH", "DELETE"].includes(String(req.method || "").toUpperCase())) return {};
  const chunks = [];
  let length = 0;
  for await (const chunk of req) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    length += buffer.length;
    if (length > MAX_BODY_BYTES) {
      const error = new Error("Request body too large");
      error.statusCode = 413;
      throw error;
    }
    chunks.push(buffer);
  }
  const raw = Buffer.concat(chunks).toString("utf8");
  if (!raw) return {};
  const contentType = String(req.headers?.["content-type"] || "").toLowerCase();
  if (contentType.includes("application/x-www-form-urlencoded")) {
    return Object.fromEntries(new URLSearchParams(raw));
  }
  if (!contentType.includes("application/json") && !contentType.includes("+json")) {
    const error = new Error("Content-Type must be application/json");
    error.statusCode = 415;
    throw error;
  }
  try { return JSON.parse(raw); }
  catch {
    const error = new Error("Invalid JSON request body");
    error.statusCode = 400;
    throw error;
  }
}

/**
 * Make a Vercel-style (req, res) handler work with Stormkit's native Node
 * IncomingMessage/ServerResponse API, while keeping local/Vercel preview use.
 */
export function withStormkitCompat(handler) {
  return async function stormkitCompatibleHandler(req, res) {
    const hasStatusJson = typeof res.status === "function" && typeof res.json === "function";
    if (!hasStatusJson) {
      res.status = function status(code) { this.statusCode = code; return this; };
      res.json = function json(payload) {
        if (!this.headersSent) this.setHeader("Content-Type", "application/json; charset=utf-8");
        if (this.statusCode == null || this.statusCode === 0) this.statusCode = 200;
        this.end(JSON.stringify(payload));
        return this;
      };
    }

    try {
      req.body = await parseBody(req);
    } catch (error) {
      const status = Number(error?.statusCode) || 400;
      return res.status(status).json({ error: status === 413 ? "Request body too large" : error.message || "Invalid request body" });
    }

    try {
      return await handler(req, res);
    } catch (error) {
      console.error("PaidMX serverless handler error:", error?.message || "unknown");
      if (res.writableEnded || res.finished) return;
      return res.status(500).json({ error: "Internal server error" });
    }
  };
}
