export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method not allowed" });
  }
  const host = String(req.headers["x-forwarded-host"] || req.headers.host || "").split(",")[0].trim().toLowerCase();
  if (!host || !/^[a-z0-9.-]+(?::\d+)?$/.test(host) || host.includes("..")) {
    return res.status(400).json({ error: "Invalid host" });
  }
  const origin = "https://" + host;
  res.setHeader("Cache-Control", "public, max-age=300, s-maxage=300");
  return res.status(200).json({
    url: origin,
    name: "PaidMX",
    iconUrl: "https://github.com/BursaliAlperen.png"
  });
}
